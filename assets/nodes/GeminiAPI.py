# --- START OF FILE GeminiAPI.py ---

import os
import json
import google.generativeai as genai # Use the official library
# Import types for SafetySetting and HarmCategory if using the library's types
# from google.generativeai import types
from io import BytesIO
from PIL import Image # For image handling
import torch # For ComfyUI tensor
import numpy as np # For tensor to numpy conversion
# cv2 and base64 are no longer needed for image encoding when using genai library

import comfy.utils # Needed for ComfyUI node structure


# Configure the Google Generative AI library to use the API key
# The library automatically looks for the GOOGLE_API_KEY environment variable.
# If not found, we'll fallback to checking the api_key_file input.

# Optional: Define the default path for the Gemini API key file
# If not defined, it will look for the API key in the environment variable "GOOGLE_API_KEY"
# Use a raw string (r"...") or double backslashes ("\\") for Windows paths
DEFAULT_API_KEY_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\gemini_api_key.txt"

# Define a default thinking budget if thinking mode is enabled
DEFAULT_THINKING_BUDGET = 4096 # You might experiment with this value

# Define available safety thresholds for the dropdown
SAFETY_THRESHOLDS = ["Block None", "Block Low", "Block Medium", "Block High"]

# Map dropdown values to API threshold constants (as strings for direct payload)
# The google-generativeai library often handles the mapping of these strings internally
SAFETY_THRESHOLD_MAP = {
    "Block None": "BLOCK_NONE",
    "Block Low": "BLOCK_LOW_AND_ABOVE",
    "Block Medium": "BLOCK_MEDIUM_AND_ABOVE",
    "Block High": "BLOCK_HIGH_AND_ABOVE",
}

# Define standard safety categories to apply the threshold to
# Using the string names as expected by the API payload / genai library
SAFETY_CATEGORIES = [
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
    # Note: Some models might have additional categories like MEDICAL, DRUG, etc.
    # Check the specific model documentation if needed.
]


class GeminiAPI:
    """
    A custom node for ComfyUI that uses the Google Gemini API for text and image generation
    via the official google-generativeai library.
    Includes optional image input (with resizing), system prompt, user instructions,
    thinking mode, and safety settings control.
    """

    CATEGORY = "Creepybits/Gemini"  # Category in ComfyUI interface
    RETURN_TYPES = ("STRING",) # Output data type
    RETURN_NAMES = ("text",)  # Output name displayed in ComfyUI

    FUNCTION = "generate_text" # Specifies the method to run when the node is executed

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),  # Input for system instructions
                "model": (["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-exp-03-25", "gemini-2.0-flash"],),  # Model selection with added models
                "max_output_tokens": ("INT", {"default": 512, "min": 1, "max": 4096}),  # Max output length, Increased default and max
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 2.0, "step": 0.1}),  # Temperature for randomness
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),  # Top-p sampling
                "top_k": ("INT", {"default": 50, "min": 1, "max": 100}),  # Top-k sampling
            },
            "optional": {
                "user_instructions": ("STRING", {"multiline": True, "default": ""}), # User instructions are now optional
                "api_key_file": ("STRING", {"default": DEFAULT_API_KEY_PATH, "multiline": False}),  # Optional file containing the API KEY
                "image": ("IMAGE",), # Image input is optional
                "resize_image_to": (["None", "512", "768", "1024"], {"default": "768"}), # Option to resize image before sending
                "thinking_mode": (["disable", "enable"], {"default": "disable"}), # Thinking mode switch
                "safety_threshold": (SAFETY_THRESHOLDS, {"default": "Block None"}), # New safety threshold input
                # Could add thinking_budget here if user wants control over the budget
                # "thinking_budget": ("INT", {"default": DEFAULT_THINKING_BUDGET, "min": 1, "max": 8192}),
            }
        }


    def generate_text(self, system_prompt, model, max_output_tokens, temperature, top_p, top_k, user_instructions="", api_key_file=None, image=None, resize_image_to="768", thinking_mode="disable", safety_threshold="Block None"):
        """
        Generates text using the Google Gemini API via the google-generativeai library.
        Handles optional image input (with resizing), system prompt, user instructions,
        thinking mode, and safety settings.
        """
        api_key = None

        # --- API Key Handling ---
        # Check environment variable first (preferred by genai library)
        api_key = os.environ.get("GOOGLE_API_KEY")

        # If not found, check the api_key_file input
        if not api_key and api_key_file and os.path.exists(api_key_file): # Added check if file exists
            try:
                with open(api_key_file, 'r') as f:
                    api_key = f.read().strip()
            except FileNotFoundError:
                # This specific error is caught by os.path.exists, so this won't be reached
                pass
            except Exception as e:
                print(f"Warning: Error reading Gemini API key file '{api_key_file}': {e}.")
        elif not api_key and api_key_file and not os.path.exists(api_key_file):
             print(f"Warning: GOOGLE_API_KEY environment variable not set and API key file not found at '{api_key_file}'.")


        if not api_key:
            return ("Error: Gemini API key not found. Please set the GOOGLE_API_KEY environment variable or provide a valid path to an API key file.",)

        # Configure the genai library with the found API key
        # This only needs to be called once, but it's safe to call multiple times.
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
             # Catch potential errors during configuration (e.g., invalid key format)
             return (f"Error configuring Gemini API with key: {e}",)


        # --- Prepare the 'contents' payload for the genai library ---
        # The genai library handles structuring the 'parts' list automatically
        # based on the types of data you provide in the contents list.
        # System instructions are often best prepended to the user prompt when
        # using the generateContent endpoint via the library.

        # Combine system prompt and user instructions for the text part
        combined_prompt_text = ""
        if system_prompt and system_prompt.strip():
             combined_prompt_text += system_prompt.strip() + "\n\n" # Add system prompt with separation

        if user_instructions and user_instructions.strip():
             combined_prompt_text += user_instructions.strip() # Add user instructions

        # Create the list of contents parts (text + optional image)
        contents = []

        # Add the text part if there is any combined prompt text
        # OR if there is no image provided (to ensure at least one part exists).
        if combined_prompt_text or image is None:
            contents.append(combined_prompt_text) # genai library accepts string directly


        # Check if image is not None before processing and adding
        pil_image = None # Initialize PIL Image variable
        if image is not None:
            try:
                # Process the image if it's provided
                image_data = image.numpy() # ComfyUI tensor to numpy
                image_data = image_data[0]  # Assuming batch size 1 (ComfyUI batch)
                image_data = (image_data * 255).astype(np.uint8)  # Scale to 0-255 range and convert to uint8

                # Convert numpy array to PIL Image
                # Handle different channel counts. Use 'RGB' for consistency with API expectations,
                # even if input is RGBA (alpha is typically ignored).
                if len(image_data.shape) == 2: # Grayscale (H, W)
                    pil_image = Image.fromarray(image_data, 'L').convert('RGB') # Convert grayscale to RGB
                elif len(image_data.shape) == 3 and image_data.shape[2] == 3: # RGB (H, W, 3)
                    pil_image = Image.fromarray(image_data, 'RGB') # 'RGB' mode
                elif len(image_data.shape) == 3 and image_data.shape[2] == 4: # RGBA (H, W, 4)
                    pil_image = Image.fromarray(image_data, 'RGBA').convert('RGB') # Convert RGBA to RGB
                else:
                    print(f"Warning: Unexpected image data shape {image_data.shape}. Attempting conversion to RGB.")
                    try:
                        # Try a general conversion to RGB if shape is unusual
                        pil_image = Image.fromarray(image_data).convert('RGB')
                    except Exception as convert_e:
                        print(f"Error converting image format: {convert_e}")
                        return ("Error: Could not process image format for API request.",)


                # --- Resize Image if specified ---
                if resize_image_to != "None" and pil_image is not None:
                    try:
                         target_size = int(resize_image_to)
                         # Resize maintaining aspect ratio, target_size is the longer dimension
                         width, height = pil_image.size # PIL uses (width, height)
                         if height > width:
                              new_height = target_size
                              new_width = int(width * (target_size / height))
                         else:
                              new_width = target_size
                              new_height = int(height * (target_size / width))

                         # Ensure new dimensions are at least 1x1
                         new_height = max(1, new_height)
                         new_width = max(1, new_width)

                         print(f"Resizing image from {width}x{height} to {new_width}x{new_height}")
                         # PIL resize uses filter=LANCZOS by default which is good quality
                         pil_image = pil_image.resize((new_width, new_height))
                    except ValueError:
                         print(f"Warning: Invalid resize_image_to value '{resize_image_to}'. Skipping resize.")
                    except Exception as e:
                         print(f"Error during image resizing: {e}. Skipping resize.")

                # Add the PIL Image object to the contents list
                if pil_image is not None:
                     contents.append(pil_image) # genai library accepts PIL Image objects directly


            except Exception as e:
                 print(f"Error processing image for API request: {e}")
                 # Return an error if image processing fails
                 return (f"Error: Failed to process image: {e}",)

        # Ensure there's at least one part in the contents list to send
        if not contents:
             return ("Error: No valid content provided. Ensure system prompt, user instructions, or image are present.",)


        # --- Construct the generationConfig payload ---
        generation_config = {
            "max_output_tokens": max_output_tokens, # <-- Changed key name to snake_case
            "temperature": temperature,
            "top_p": top_p, # <-- Changed key name to snake_case
            "top_k": top_k, # <-- Changed key name to snake_case
            # Note: Seed parameter removed as it caused a 400 error previously.
            # The Gemini API documentation doesn't explicitly mention a seed parameter
            # for this endpoint at the time of writing.
        }

        # --- Add thinkingConfig if thinking_mode is enabled ---
        # Note: thinkingConfig is generally part of generationConfig.
        if thinking_mode == "enable":
             # The genai library expects 'thinking_config' (snake_case) containing 'thinking_budget' (snake_case)
             generation_config["thinking_config"] = {"thinking_budget": DEFAULT_THINKING_BUDGET} # <-- Changed key names
             print(f"Thinking mode enabled with budget {DEFAULT_THINKING_BUDGET}.")
             # Note: Model support for thinking mode might vary. API may ignore this config.


        # --- Construct the safety_settings payload ---
        safety_settings = []
        # Get the API threshold value from the map
        api_threshold = SAFETY_THRESHOLD_MAP.get(safety_threshold, "BLOCK_NONE") # Default to BLOCK_NONE if key not found

        # Add safety settings for each category if the threshold is not 'BLOCK_NONE'
        if api_threshold != "BLOCK_NONE":
            for category_name in SAFETY_CATEGORIES:
                safety_settings.append({
                    "category": category_name,
                    "threshold": api_threshold
                })
            print(f"Applying safety threshold '{api_threshold}' to categories: {SAFETY_CATEGORIES}")
        else:
            print("Safety threshold set to 'Block None'. No safety settings applied.")


        # --- Get the Generative Model ---
        try:
            # Use genai.GenerativeModel to get the specific model
            model_instance = genai.GenerativeModel(model)
        except Exception as e:
            print(f"Error getting model '{model}': {e}")
            # Check if the error is due to an invalid model name
            if "Invalid model" in str(e):
                 return (f"Error: Invalid model name '{model}'. Check model availability.",)
            return (f"Error: Could not get Gemini model '{model}'. Check model name, API status, or internet connection: {e}",)


        # --- Send API Request using genai library ---
        try:
            # The genai library handles the request format (including roles implicitly for a single turn)
            # and sending the request to the correct endpoint.
            # Pass the constructed safety_settings list to the generate_content call
            response = model_instance.generate_content(
                contents, # This is the list of text strings and PIL Images
                generation_config=generation_config,
                safety_settings=safety_settings, # <--- Added safety settings here
            )

            # The response object from the library has attributes, not just text
            # Access the generated text. The structure depends on the response.
            # If generation fails due to safety or other reasons, response.text might be empty
            # or response.candidates might be missing/empty.
            generated_text = ""
            # Primary way to get text from a successful generation:
            if hasattr(response, 'text'):
                 generated_text = response.text
            # Fallback/check if the above is empty or missing:
            # Note: Accessing response.candidates can itself raise exceptions if candidates is None or empty
            elif hasattr(response, 'candidates') and response.candidates:
                 try:
                     # Try accessing the text from the first candidate's first part
                      # response.candidates is a list of Candidate objects.
                      # Candidate objects have a .content attribute, which is a Content object.
                      # Content objects have a .parts attribute, which is a list of Part objects.
                      # Part objects have a .text attribute.
                      if hasattr(response.candidates[0], 'content') and response.candidates[0].content and \
                         hasattr(response.candidates[0].content, 'parts') and response.candidates[0].content.parts:
                          generated_text = response.candidates[0].content.parts[0].text
                 except (AttributeError, IndexError, KeyError):
                      # Fallback if expected structure isn't found
                      print("Warning: Could not extract text from response.candidates structure.")
                      # We don't print the full structure here to avoid spamming console


            # Check if generated_text is still empty, could be due to safety filters or other issues
            if not generated_text:
                 print("Generated text is empty or extraction failed.")
                 # Print more detailed info in case of no text generation
                 # print(f"Full response object (or part): {response}") # May be too verbose

                 # Check prompt feedback in the response object if available
                 # The prompt_feedback attribute exists if the prompt was blocked or had issues
                 if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                     print("Prompt Feedback:")
                     feedback_info = {}
                     # Check if block_reason exists and is not UNASSIGNED (which is default for no block)
                     if hasattr(response.prompt_feedback, 'block_reason') and response.prompt_feedback.block_reason and hasattr(response.prompt_feedback.block_reason, 'name') and response.prompt_feedback.block_reason.name != 'UNASSIGNED':
                          print(f"  Block Reason: {response.prompt_feedback.block_reason.name}")
                          feedback_info['block_reason'] = response.prompt_feedback.block_reason.name # Use .name to get string enum

                     if hasattr(response.prompt_feedback, 'safety_ratings') and response.prompt_feedback.safety_ratings:
                         print("  Safety Ratings:")
                         feedback_info['safety_ratings'] = []
                         for rating in response.prompt_feedback.safety_ratings:
                             # Only print/report safety ratings that actually blocked something (usually PROBABILITY_UNSPECIFIED or higher)
                             if hasattr(rating, 'probability') and hasattr(rating.probability, 'name') and rating.probability.name != 'UNSPECIFIED':
                                 rating_info = {"category": rating.category.name, "probability": rating.probability.name} # Use .name for string enums
                                 print(f"    Category: {rating_info['category']}, Probability: {rating_info['probability']}")
                                 feedback_info['safety_ratings'].append(rating_info)

                     # Provide a user-friendly error message based on feedback
                     if 'block_reason' in feedback_info:
                          return (f"Error: Content generation blocked due to {feedback_info['block_reason']}. Check console for safety feedback.",)
                     elif 'safety_ratings' in feedback_info and feedback_info['safety_ratings']:
                          # If no block reason, but safety ratings are high, it still might have influenced output
                          return ("Error: No text generated. High safety ratings. Check console for details.",)
                     # Fallback if prompt_feedback exists but doesn't have block reason or significant safety issues
                     return ("Error: No text generated. API returned empty content/candidates. Check Prompt Feedback in console.",)
                 else:
                      # If no prompt feedback object, or it's empty, or doesn't have expected info
                      # Check if candidates list was explicitly empty (often means blocked)
                      if hasattr(response, 'candidates') and not response.candidates:
                           return ("Error: API returned no candidates (likely blocked). No prompt feedback details available.",)
                      # If candidates exist but text wasn't extracted, or other unknown issue
                      return ("Error: No text generated from the API and no specific feedback provided. Check console.",)


            return (generated_text,) # Return the generated text


        # --- Error Handling (for genai library exceptions) ---
        # Catch the most general Python exception as a fallback
        # This will catch any error that occurs within the try block
        except Exception as e: # Catching general Exception as previous genai-specific ones failed
            print(f"An error occurred during Gemini API call: {e}")
            # Attempt to get error details from the exception's response attribute if available
            error_message = str(e) # Default error message
            # Check if the exception object has a 'response' attribute
            if hasattr(e, 'response') and e.response:
                 # Try to parse the response text as JSON to get API specific error message
                 if hasattr(e.response, 'text'):
                      try:
                           error_json = json.loads(e.response.text)
                           if 'error' in error_json and 'message' in error_json['error']:
                                api_error_message = error_json['error']['message']
                                print(f"API Error Message from response: {api_error_message}")
                                error_message = f"API Error: {api_error_message}"
                           elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                # Catch standard HTTP error details if not JSON
                                error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                      except (json.JSONDecodeError, AttributeError):
                           # If response text is not JSON or AttributeError accessing parts
                           if hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                # Still provide HTTP error if available
                                error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                           # Otherwise, error_message remains the original string representation of the exception
                           pass # Ignore if response text is not JSON or doesn't have expected API error format

                 elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                      # Handle cases where response object exists but no text attribute (e.g., non-text response types)
                      error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"

            return (f"Error: An error occurred during Gemini API call: {error_message}",)


# --- ComfyUI Node Mappings ---
NODE_CLASS_MAPPINGS = {
    "GeminiAPI": GeminiAPI,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiAPI": "Gemini 2.5 Flash/Pro API (Creepybits)", # Updated display name
}

# --- END OF FILE GeminiAPI.py ---

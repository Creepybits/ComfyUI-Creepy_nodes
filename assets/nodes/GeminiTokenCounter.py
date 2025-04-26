# --- START OF FILE TokenCounter.py ---

import os
import json
import google.generativeai as genai
from PIL import Image # For image handling
import torch # For ComfyUI tensor
import numpy as np # For tensor to numpy conversion
# time, torchaudio, pathlib, absltest, UnitTests, etc. are not needed for the ComfyUI node

# Configure the Google Generative AI library to use the API key
# The library automatically looks for the GOOGLE_API_KEY environment variable.
# If not found, we'll fallback to checking the api_key_file input.

# Optional: Define the default path for the Gemini API key file
# If not defined, it will look for the API key in the environment variable "GOOGLE_API_KEY"
# Use a raw string (r"...") or double backslashes ("\\") for Windows paths
# Make sure this path matches where you expect the API key file to be
DEFAULT_API_KEY_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\gemini_api_key.txt"


class GeminiTokenCounter:
    """
    A ComfyUI node to count tokens for text and image inputs using the
    Google Gemini API via the google-generativeai library.
    Reports input token count and model limits.
    """

    CATEGORY = "Creepybits/Gemini"  # Category in ComfyUI interface
    RETURN_TYPES = ("STRING",) # Output data type
    RETURN_NAMES = ("token_report",)  # Output name displayed in ComfyUI

    FUNCTION = "get_token_counts" # Specifies the method to run when the node is executed

    @classmethod
    def INPUT_TYPES(s):
        # Note: Inputs here define what appears in ComfyUI's node interface.
        # The method signature for the FUNCTION must match these inputs.
        return {
            "required": {
                # Using models likely supported by genai for token counting
                "model": (["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-exp-03-25", "gemini-2.0-flash"],),
                 # Add more models if google-generativeai library supports counting tokens for them
            },
            "optional": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),  # Optional system instructions input
                "text_input": ("STRING", {"multiline": True, "default": ""}), # Optional text input
                "image_input": ("IMAGE",), # Optional image input
                "api_key_file": ("STRING", {"default": DEFAULT_API_KEY_PATH, "multiline": False}),  # Optional file containing the API KEY
                # We won't include image resizing in the counter node itself,
                # as the 'count_tokens' method doesn't account for it - it counts the full PIL Image.
                # Resizing should be done *before* sending the image to this node if needed for the count.
            }
        }

    def get_token_counts(self, model, system_prompt="", text_input="", image_input=None, api_key_file=None):
        """
        Counts tokens for the provided text and/or image input using the specified model
        and reports the counts and model limits.
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
        try:
            # This only needs to be called once per API key change, but is safe to call repeatedly.
            genai.configure(api_key=api_key)
        except Exception as e:
             # Catch potential errors during configuration (e.g., invalid key format)
             return (f"Error configuring Gemini API with key: {e}",)

        # --- Prepare content for counting ---
        # The count_tokens method accepts a list of parts (strings, PIL.Images)
        # Include system_prompt and text_input in the content list.
        content_parts_for_counting = []

        # Add system prompt text if it exists and is not just whitespace
        if system_prompt and system_prompt.strip():
            content_parts_for_counting.append(system_prompt.strip()) # Add system prompt

        # Add user text input if it exists and is not just whitespace
        if text_input and text_input.strip():
            # Add a separator if system prompt was also included
            if system_prompt and system_prompt.strip():
                 content_parts_for_counting.append("\n\n") # Add separation between system and user text
            content_parts_for_counting.append(text_input.strip()) # Add user text


        # Process image if provided
        pil_image = None # Initialize PIL Image variable
        if image_input is not None:
            try:
                # Process the image from ComfyUI tensor to PIL Image
                image_data = image_input.numpy() # ComfyUI tensor to numpy
                image_data = image_data[0]  # Assuming batch size 1 (ComfyUI batch)
                image_data = (image_data * 255).astype(np.uint8)  # Scale to 0-255 range and convert to uint8

                # Convert numpy array to PIL Image
                # Handle different channel counts. Use 'RGB' for consistency.
                if len(image_data.shape) == 2: # Grayscale (H, W)
                    pil_image = Image.fromarray(image_data, 'L').convert('RGB') # Convert grayscale to RGB
                elif len(image_data.shape) == 3 and image_data.shape[2] == 3: # RGB (H, W, 3)
                    pil_image = Image.fromarray(image_data, 'RGB') # 'RGB' mode
                elif len(image_data.shape) == 3 and image_data.shape[2] == 4: # RGBA (H, W, 4)
                    pil_image = Image.fromarray(image_data, 'RGBA').convert('RGB') # Convert RGBA to RGB (drops alpha)
                else:
                    print(f"Warning: Unexpected image data shape {image_data.shape}. Attempting conversion to RGB for counting.")
                    try:
                        # Try a general conversion to RGB if shape is unusual
                        pil_image = Image.fromarray(image_data).convert('RGB')
                    except Exception as convert_e:
                        print(f"Error converting image format for counting: {convert_e}")
                        return ("Error: Could not process image format for API request.",)

                # Add the PIL Image object to the content parts list
                if pil_image is not None:
                     content_parts_for_counting.append(pil_image) # genai library accepts PIL Image objects directly


            except Exception as e:
                 print(f"Error processing image for token counting: {e}")
                 # Return an error if image processing fails
                 return (f"Error: Failed to process image for token counting: {e}",)

        # Ensure there's at least some content to count
        # If the list is empty, it means system prompt, text_input, and image_input were all empty/None.
        if not content_parts_for_counting:
             return ("Error: No text or image content provided to count tokens for. Please provide a system prompt, text input, or an image.",)


        # --- Get the Generative Model instance ---
        try:
            # Use genai.GenerativeModel to get the specific model for counting
            # The count_tokens method is available on the model instance
            model_instance = genai.GenerativeModel(model)
        except Exception as e:
            print(f"Error getting model '{model}' for counting: {e}")
            # Check if the error is due to an invalid model name
            if "Invalid model" in str(e) or "Model not found" in str(e):
                 return (f"Error: Invalid model name '{model}'. Check model availability for counting.",)
            return (f"Error: Could not get Gemini model '{model}' for counting. Check model name or API status: {e}",)

        # --- Count Tokens ---
        token_count = 0
        try:
            # Call count_tokens with the combined list of content parts
            # REMOVED the system_instruction keyword argument here.
            count_response = model_instance.count_tokens(content_parts_for_counting)

            # The count_tokens response is an object with a .total_tokens attribute
            if hasattr(count_response, 'total_tokens'):
                token_count = count_response.total_tokens
                print(f"Successfully counted tokens for input. Total input tokens: {token_count}")
            else:
                # Fallback if the response structure is unexpected
                print(f"Warning: Count tokens response object has no 'total_tokens' attribute. Full response: {count_response}")
                return ("Error: Could not get token count from API response.",)

        except Exception as e: # Catch any errors during the count_tokens API call
            print(f"Error counting tokens for model '{model}': {e}")
            # Provide more specific error if possible
            error_message = str(e)
            # Try to extract API error from response if available in exception (less common for count_tokens errors)
            if hasattr(e, 'response') and e.response and hasattr(e.response, 'text'):
                 try:
                      error_json = json.loads(e.response.text)
                      if 'error' in error_json and 'message' in error_json['error']:
                           api_error_message = error_json['error']['message']
                           print(f"API Error Message from count_tokens response: {api_error_message}")
                           error_message = f"API Error: {api_error_message}"
                      elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                            error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                 except (json.JSONDecodeError, AttributeError):
                      pass # Ignore if response text is not JSON or not structured as expected
            return (f"Error counting tokens: {error_message}",)


        # --- Get Model Limits ---
        input_limit = "N/A"
        output_limit = "N/A"
        try:
            # Use genai.get_model() to get model information including limits
            model_info = genai.get_model(model)
            # Check if attributes exist before accessing
            if hasattr(model_info, 'input_token_limit'):
                 input_limit = model_info.input_token_limit
            if hasattr(model_info, 'output_token_limit'):
                 output_limit = model_info.output_token_limit

            print(f"Successfully retrieved limits for model '{model}'. Input: {input_limit}, Output: {output_limit}")

        except Exception as e: # Catch errors getting model info
            print(f"Warning: Could not retrieve limits for model '{model}': {e}")
            # Limits will remain "N/A" if retrieval failed


        # --- Construct Report String ---
        report = f"--- Gemini Token Report ---"
        report += f"\nModel: {model}"
        report += f"\n"
        report += f"\nInput Tokens (Estimate for System Prompt + User Text + Image): {token_count}"
        # Note: This is the *input* token count estimate *before* generation.
        # The actual tokens consumed by generate_content will include the generated output tokens as well.

        report += f"\n"
        report += f"\nModel Limits:"
        report += f"\n  Max Input Tokens (Context Window): {input_limit}"
        report += f"\n  Max Output Tokens (Response): {output_limit}"
        # Total context window is typically Input Limit + Output Limit, but the API docs
        # sometimes just refer to input_token_limit as the total context window.
        # Let's show both explicitly if available.


        # --- Info that is NOT directly available ---
        report += f"\n"
        report += f"\n--- Additional Information ---"
        report += f"\nTotal tokens used across multiple API calls (e.g., today) is NOT available directly via the API methods used here. This is typically tracked in your Google Cloud billing or usage reports."


        # --- Return the report ---
        return (report,)

# --- ComfyUI Node Mappings ---
NODE_CLASS_MAPPINGS = {
    "GeminiTokenCounter": GeminiTokenCounter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiTokenCounter": "Gemini Token Counter (Creepybits)", # Node name in ComfyUI interface
}

# --- END OF FILE TokenCounter.py ---

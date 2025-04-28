# --- START OF FILE GeminiAudioAnalyzer.py ---

# Gemini_Flash_Node.py
import os
import json
import base64
import requests
import google.generativeai as genai
from io import BytesIO
from PIL import Image
import torch
import torchaudio
import numpy as np

# Define the default path for the Gemini API key file
# Use a raw string (r"...") or double backslashes ("\\") for Windows paths
DEFAULT_API_KEY_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\gemini_api_key.txt"

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


class GeminiAudioAnalyzer:
    """
    A custom node for ComfyUI that uses the Google Gemini API for text generation
    with audio analysis capabilities.
    Loads API key from input field or default file.
    """

    CATEGORY = "Creepybits/Audio"  # Category in ComfyUI interface
    RETURN_TYPES = ("STRING",) # Output data type (a single string)
    RETURN_NAMES = ("generated_content",)  # Output name displayed in ComfyUI
    FUNCTION = "generate_content" # Specifies the method to run when the node is executed

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Analyze the situation in details.", "multiline": True}),
                "input_type": (["text", "audio"], {"default": "text"}), # Added text option
                "model_version": (["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-exp-03-25", "gemini-2.0-flash"], {"default": "gemini-2.0-flash"}), # Added new models
                "operation_mode": (["analysis", "generate_images"], {"default": "analysis"}), # operation_mode - seems unused in generate_content but kept as in original
            },
            "optional": {
                "Additional_Context": ("STRING", {"default": "", "multiline": True}), # Renamed from context to Additional_Context for clarity
                "audio": ("AUDIO", ), # Added audio input type
                "api_key": ("STRING", {"default": "", "multiline": False}), # API Key input field, defaults to empty string
                "max_output_tokens": ("INT", {"default": 2048, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.1}),
                "safety_threshold": (SAFETY_THRESHOLDS, {"default": "Block None"}),
            }
        }

    def __init__(self):
        # Note: Chat history is not currently used in generate_content (single turn)
        self.chat_history = []  # Placeholder for chat history if multi-turn was implemented

    def load_api_key(self, api_key=""):
        """
        Loads the API key from the provided string parameter or the default file.
        Prioritizes the provided string.
        """
        # Check if the api_key parameter (from the node input) is provided and not empty
        if api_key and api_key.strip(): # Added .strip() here for robustness
            # print(f"[AudioAnalyzer load_api_key] Using API key from node input.") # Debug print removed
            return api_key.strip()  # Use the provided key if available, ensuring it's stripped

        # Attempt to read from the default file path if input was empty or whitespace
        # print(f"[AudioAnalyzer load_api_key] Input empty, attempting file load from: {DEFAULT_API_KEY_PATH}") # Debug print removed
        try:
            # Attempt to read from the default file path
            with open(DEFAULT_API_KEY_PATH, "r") as f:
                file_content = f.read()
                stripped_key = file_content.strip()

                # Check if the key read from the file is not empty after stripping
                if stripped_key:
                     # print(f"[AudioAnalyzer load_api_key] File key loaded successfully.") # Debug print removed
                     return stripped_key
                else:
                     print(f"[AudioAnalyzer load_api_key] Warning: API key file at '{DEFAULT_API_KEY_PATH}' is empty or contains only whitespace.")
                     return None # Explicitly return None if file is empty

        except FileNotFoundError:
            print(f"[AudioAnalyzer load_api_key] Warning: API key file not found at {DEFAULT_API_KEY_PATH}. Tried to load because node input was empty.")
            return None # Return None if the file doesn't exist
        except Exception as e:
            print(f"[AudioAnalyzer load_api_key] Warning: Error reading API key file: {e}")
            return None # Return None for other file reading errors


    def prepare_content(self, prompt, input_type, Additional_Context=None, audio=None):
        """Prepares the content for the Gemini API based on the input type."""
        # Combine prompt and additional context for text input
        text_content = prompt if not Additional_Context else f"{prompt}\n\n{Additional_Context.strip()}" # Added strip and separation

        if input_type == "text":
            # For text-only input, the contents list contains a single text part
            # The genai library handles the structure if you just pass the string
            # return [{"text": text_content}] # Old way, genai library is more flexible
            return [text_content] # Pass the string directly

        elif input_type == "audio" and audio is not None:
            # Ensure text content is included along with audio for multimodal models
            content_parts = []
            if text_content.strip(): # Only add text part if there's content
                 content_parts.append({"text": text_content.strip()})

            # Audio processing (assuming 'audio' is a dictionary with 'waveform' and 'sample_rate' from another ComfyUI node)
            try:
                waveform = audio["waveform"]
                sample_rate = audio["sample_rate"]

                # Ensure waveform is 2D [channels, samples] for torchaudio.save
                if waveform.dim() == 3: # Assuming [batch, channels, samples] from ComfyUI AUDIO type
                    waveform = waveform.squeeze(0) # Remove batch dimension
                elif waveform.dim() == 1: # Assuming [samples]
                    waveform = waveform.unsqueeze(0) # Add channel dimension

                # If multiple channels, average them (simple mono conversion)
                if waveform.shape[0] > 1:
                    print(f"[AudioAnalyzer prepare_content] Warning: Input audio has {waveform.shape[0]} channels. Converting to mono by averaging.")
                    waveform = torch.mean(waveform, dim=0, keepdim=True)

                # Resample to 16kHz if needed (Gemini expects 16kHz for audio)
                if sample_rate != 16000:
                    print(f"[AudioAnalyzer prepare_content] Resampling audio from {sample_rate}Hz to 16000Hz.")
                    waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)

                # Save to a BytesIO buffer in WAV format
                buffer = BytesIO()
                torchaudio.save(buffer, waveform, 16000, format="WAV")
                audio_bytes = buffer.getvalue()

                # Add the audio part as inline data
                content_parts.append({
                    "inline_data": {
                        "mime_type": "audio/wav",
                        "data": base64.b64encode(audio_bytes).decode('utf-8') # Base64 encode the audio bytes
                    }
                })

            except KeyError as e:
                 print(f"[AudioAnalyzer prepare_content] Error: Missing expected key in audio input: {e}")
                 raise ValueError(f"Invalid audio input format: Missing key {e}") from e
            except Exception as e:
                 print(f"[AudioAnalyzer prepare_content] Error processing audio: {e}")
                 raise ValueError(f"Failed to process audio input: {e}") from e

            # Return the list of parts (text + audio)
            return content_parts

        else:
            # Handle cases where audio is selected but not provided, or input_type is invalid
            if input_type == "audio" and audio is None:
                 raise ValueError("Input type set to 'audio', but no audio input was provided.")
            else:
                 raise ValueError(f"Invalid input_type: '{input_type}'. Must be 'text' or 'audio'.")


    def generate_content(self, prompt, input_type, model_version="gemini-2.0-flash",
                        operation_mode="analysis", Additional_Context=None, # operation_mode is unused in this function
                        audio=None, api_key="", max_output_tokens=8192, # api_key parameter receives input from node field
                        safety_threshold="Block None", temperature=0.4):
        """Generate content using Gemini model with various input types (text, audio)."""

        # --- API Key Loading ---
        # This calls load_api_key, which handles checking input field vs. file
        resolved_api_key = self.load_api_key(api_key)

        # Check if a valid API key was successfully obtained
        if not resolved_api_key or not resolved_api_key.strip(): # Added .strip() check here too for robustness
            # print("[AudioAnalyzer generate_content] API key not resolved.") # Debug print removed
            # Return a tuple with an error message for ComfyUI string output
            return ("Error: Gemini API key not found or loaded for Audio Analyzer. Please provide key in node input, set GOOGLE_API_KEY env var, or ensure valid key in default file. Check console output for details.",)

        # --- Configure Gemini Library ---
        try:
            # Configure the genai library with the resolved API key
            genai.configure(api_key=resolved_api_key)
            print("[AudioAnalyzer] Gemini API Key configured successfully.") # Keep this - useful confirmation

        except Exception as e:
            # Catch potential errors during configuration (e.g., invalid key format)
             error_message_detail = str(e)
             if hasattr(e, 'response') and e.response:
                  if hasattr(e.response, 'text'):
                       try:
                            error_json = json.loads(e.response.text)
                            if 'error' in error_json and 'message' in error_json['error']:
                                 api_error_message = error_json['error']['message']
                                 error_message_detail = f"API Error during configuration: {api_error_message}"
                            # Add checks for status_code/reason if needed, similar to main exception
                       except (json.JSONDecodeError, AttributeError):
                            pass # Keep original error message if JSON parsing fails

             print(f"[AudioAnalyzer] Error configuring Gemini API: {error_message_detail}")
             return (f"Error configuring Gemini API: {error_message_detail}",)


        # --- Configure Safety Settings ---
        safety_settings = [] # Initialize safety settings list
        api_threshold = SAFETY_THRESHOLD_MAP.get(safety_threshold, "BLOCK_NONE") # Get API threshold string

        if api_threshold != "BLOCK_NONE":
            # Apply the selected threshold to standard safety categories
            for category_name in SAFETY_CATEGORIES:
                safety_settings.append({
                    "category": category_name,
                    "threshold": api_threshold
                })
            print(f"[AudioAnalyzer] Applying safety threshold '{api_threshold}' to categories: {SAFETY_CATEGORIES}")
        else:
            print("[AudioAnalyzer] Safety threshold set to 'Block None'. No safety settings applied.")

        # --- Configure Generation Parameters ---
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            # Add other parameters if needed, e.g., top_p, top_k
            # top_p=...
            # top_k=...
        )
        # print(f"[AudioAnalyzer] Generation config: {generation_config}") # Optional: print full config


        # --- Get the Generative Model Instance ---
        try:
            # Use genai.GenerativeModel to get the specific model
            # Pass safety_settings and generation_config here
            model = genai.GenerativeModel(
                model_name=model_version,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            print(f"[AudioAnalyzer] Model instance created for '{model_version}'.") # Keep this - useful confirmation

        except Exception as e:
            print(f"[AudioAnalyzer] Error getting model '{model_version}': {e}")
            # Check if the error is due to an invalid model name
            if "Invalid model" in str(e):
                 return (f"Error: Invalid model name '{model_version}'. Check model availability.",)
            # Fallback error message
            return (f"Error: Could not get Gemini model '{model_version}'. Check model name, API status, or internet connection: {e}",)


        # --- Prepare Content (Text + Optional Audio) ---
        try:
            content_parts = self.prepare_content(prompt, input_type, Additional_Context, audio)
            # print(f"[AudioAnalyzer] Content parts prepared: {content_parts}") # Optional: print content parts
        except ValueError as e: # Catch specific errors from prepare_content
             print(f"[AudioAnalyzer] Error during content preparation: {e}")
             return (f"Error preparing content: {e}",)
        except Exception as e: # Catch any other unexpected errors during preparation
             print(f"[AudioAnalyzer] Unexpected error during content preparation: {e}")
             return (f"Unexpected error preparing content: {e}",)


        # --- Send API Request ---
        try:
            # The genai library handles the request format and sending
            print("[AudioAnalyzer] Sending generate_content request...") # Keep this - useful confirmation
            response = model.generate_content(
                contents=content_parts,
                # Safety settings and generation config are typically passed when creating the model instance
                # Passing them again here depends on the library version/design, but often not needed if done in init.
                # If your previous version worked with them here, you might need to add them back.
                # generation_config=generation_config # Example if needed
                # safety_settings=safety_settings, # Example if needed
            )
            print("[AudioAnalyzer] API request finished.") # Keep this - useful confirmation


            # --- Process Response ---
            generated_content = ""
            # Check if the response object has a 'text' attribute (common for success)
            if hasattr(response, 'text'):
                 generated_content = response.text
            # Note: Could add more sophisticated checks here if response.text is often empty but candidates exist

            # If no text was directly generated, check for block reasons or empty candidates
            if not generated_content:
                 print("[AudioAnalyzer] Generated text is empty or extraction failed.") # Keep this warning

                 # Check prompt feedback in the response object if available (e.g., safety blocks)
                 if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                     print("[AudioAnalyzer] Prompt Feedback received:") # Keep this
                     feedback_info = {}
                     # Check if block_reason exists and is not UNASSIGNED
                     if hasattr(response.prompt_feedback, 'block_reason') and response.prompt_feedback.block_reason and hasattr(response.prompt_feedback.block_reason, 'name') and response.prompt_feedback.block_reason.name != 'UNASSIGNED':
                          print(f"  Block Reason: {response.prompt_feedback.block_reason.name}") # Keep this
                          feedback_info['block_reason'] = response.prompt_feedback.block_reason.name

                     if hasattr(response.prompt_feedback, 'safety_ratings') and response.prompt_feedback.safety_ratings:
                         print("  Safety Ratings:") # Keep this
                         feedback_info['safety_ratings'] = []
                         for rating in response.prompt_feedback.safety_ratings:
                             # Only print/report safety ratings that are not UNSPECIFIED probability
                             if hasattr(rating, 'probability') and hasattr(rating.probability, 'name') and rating.probability.name != 'UNSPECIFIED':
                                 rating_info = {"category": rating.category.name, "probability": rating.probability.name}
                                 print(f"    Category: {rating_info['category']}, Probability: {rating_info['probability']}") # Keep this
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


            # print(f"[AudioAnalyzer] Generated content length: {len(generated_content)}") # Optional: print length
            # ComfyUI nodes returning STRING should return a tuple containing the string
            return (generated_content,)

        # --- Error Handling (for exceptions during API call) ---
        except Exception as e:
            # Catch any exception during the API call itself
            print(f"[AudioAnalyzer] An error occurred during Gemini API call: {e}") # Keep this basic error print

            # Attempt to get more specific error details from the exception if it's an API error
            error_message_detail = str(e) # Default error message is the exception string
            if hasattr(e, 'response') and e.response:
                 if hasattr(e.response, 'text'):
                      try:
                           error_json = json.loads(e.response.text)
                           if 'error' in error_json and 'message' in error_json['error']:
                                api_error_message = error_json['error']['message']
                                print(f"[AudioAnalyzer] API Error Message from response: {api_error_message}") # Keep this
                                error_message_detail = f"API Error: {api_error_message}"
                           elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                # Catch standard HTTP error details if not JSON
                                error_message_detail = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                      except (json.JSONDecodeError, AttributeError):
                           # If response text is not JSON or AttributeError accessing parts
                           if hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                error_message_detail = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                           pass # Use the original exception string if cannot extract API specific

                 elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                      error_message_detail = f"HTTP Error: {e.response.status_code} {e.response.reason}"

            # Return a tuple with the error message for ComfyUI string output
            return (f"Error: An error occurred during Gemini API call: {error_message_detail}",)


# --- ComfyUI Node Mappings ---
NODE_CLASS_MAPPINGS = {
    "GeminiAudioAnalyzer": GeminiAudioAnalyzer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiAudioAnalyzer": "Gemini Audio Analyzer (Creepybits)",
}

# --- END OF FILE GeminiAudioAnalyzer.py ---

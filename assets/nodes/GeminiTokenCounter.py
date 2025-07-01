import os
import json
import google.generativeai as genai
from PIL import Image
import torch
import numpy as np

DEFAULT_API_KEY_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\gemini_api_key.txt"


class GeminiTokenCounter:
    """
    A ComfyUI node to count tokens for text and image inputs using the
    Google Gemini API via the google-generativeai library.
    Reports input token count and model limits.
    """

    CATEGORY = "Creepybits/Gemini"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("token_report",)

    FUNCTION = "get_token_counts"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-exp-03-25", "gemini-2.0-flash"],),
            },
            "optional": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),
                "text_input": ("STRING", {"multiline": True, "default": ""}),
                "image_input": ("IMAGE",),
                "api_key_file": ("STRING", {"default": DEFAULT_API_KEY_PATH, "multiline": False}),
            }
        }

    def get_token_counts(self, model, system_prompt="", text_input="", image_input=None, api_key_file=None):
        """
        Counts tokens for the provided text and/or image input using the specified model
        and reports the counts and model limits.
        """
        api_key = None

        # --- API Key Handling ---
        api_key = os.environ.get("GOOGLE_API_KEY")

        if not api_key and api_key_file and os.path.exists(api_key_file):
            try:
                with open(api_key_file, 'r') as f:
                    api_key = f.read().strip()
            except Exception as e:
                print(f"Warning: Error reading Gemini API key file '{api_key_file}': {e}.")
        elif not api_key and api_key_file and not os.path.exists(api_key_file):
             print(f"Warning: GOOGLE_API_KEY environment variable not set and API key file not found at '{api_key_file}'.")


        if not api_key:
            return ("Error: Gemini API key not found. Please set the GOOGLE_API_KEY environment variable or provide a valid path to an API key file.",)

        try:
            genai.configure(api_key=api_key)
        except Exception as e:
             return (f"Error configuring Gemini API with key: {e}",)

        # --- Prepare content for counting ---
        content_parts_for_counting = []

        if system_prompt and system_prompt.strip():
            content_parts_for_counting.append(system_prompt.strip())

        if text_input and text_input.strip():
            if system_prompt and system_prompt.strip():
                 content_parts_for_counting.append("\n\n")
            content_parts_for_counting.append(text_input.strip())


        pil_image = None
        if image_input is not None:
            try:
                image_data = image_input.numpy()
                image_data = image_data[0]
                image_data = (image_data * 255).astype(np.uint8)

                if len(image_data.shape) == 2:
                    pil_image = Image.fromarray(image_data, 'L').convert('RGB')
                elif len(image_data.shape) == 3 and image_data.shape[2] == 3:
                    pil_image = Image.fromarray(image_data, 'RGB')
                elif len(image_data.shape) == 3 and image_data.shape[2] == 4:
                    pil_image = Image.fromarray(image_data, 'RGBA').convert('RGB')
                else:
                    return ("Error: Could not process image format for API request.",)

                if pil_image is not None:
                     content_parts_for_counting.append(pil_image)


            except Exception as e:
                 return (f"Error: Failed to process image for token counting: {e}",)

        if not content_parts_for_counting:
             return ("Error: No text or image content provided to count tokens for. Please provide a system prompt, text input, or an image.",)


        # --- Get the Generative Model instance ---
        try:
            model_instance = genai.GenerativeModel(model)
        except Exception as e:
            if "Invalid model" in str(e) or "Model not found" in str(e):
                 return (f"Error: Invalid model name '{model}'. Check model availability for counting.",)
            return (f"Error: Could not get Gemini model '{model}' for counting. Check model name or API status: {e}",)

        # --- Count Tokens ---
        token_count = 0
        try:
            count_response = model_instance.count_tokens(content_parts_for_counting)

            if hasattr(count_response, 'total_tokens'):
                token_count = count_response.total_tokens
            else:
                return ("Error: Could not get token count from API response.",)

        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response and hasattr(e.response, 'text'):
                 try:
                      error_json = json.loads(e.response.text)
                      if 'error' in error_json and 'message' in error_json['error']:
                           api_error_message = error_json['error']['message']
                           error_message = f"API Error: {api_error_message}"
                      elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                            error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                 except (json.JSONDecodeError, AttributeError):
                      pass
            return (f"Error counting tokens: {error_message}",)


        # --- Get Model Limits ---
        input_limit = "N/A"
        output_limit = "N/A"
        try:
            model_info = genai.get_model(model)
            if hasattr(model_info, 'input_token_limit'):
                 input_limit = model_info.input_token_limit
            if hasattr(model_info, 'output_token_limit'):
                 output_limit = model_info.output_token_limit

        except Exception:
            pass


        # --- Construct Report String ---
        report = f"--- Gemini Token Report ---"
        report += f"\nModel: {model}"
        report += f"\n"
        report += f"\nInput Tokens (Estimate for System Prompt + User Text + Image): {token_count}"

        report += f"\n"
        report += f"\nModel Limits:"
        report += f"\n  Max Input Tokens (Context Window): {input_limit}"
        report += f"\n  Max Output Tokens (Response): {output_limit}"

        report += f"\n"
        report += f"\n--- Additional Information ---"
        report += f"\nTotal tokens used across multiple API calls (e.g., today) is NOT available directly via the API methods used here. This is typically tracked in your Google Cloud billing or usage reports."


        # --- Return the report ---
        return (report,)

NODE_CLASS_MAPPINGS = {
    "GeminiTokenCounter": GeminiTokenCounter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiTokenCounter": "Gemini Token Counter (Creepybits)",
}

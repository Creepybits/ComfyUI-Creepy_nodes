import os
import json
import google.generativeai as genai
from io import BytesIO
from PIL import Image
import torch
import numpy as np

import comfy.utils


DEFAULT_API_KEY_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\gemini_api_key.txt"
DEFAULT_THINKING_BUDGET = 4096

SAFETY_THRESHOLDS = ["Block None", "Block Low", "Block Medium", "Block High"]

SAFETY_THRESHOLD_MAP = {
    "Block None": "BLOCK_NONE",
    "Block Low": "BLOCK_LOW_AND_ABOVE",
    "Block Medium": "BLOCK_MEDIUM_AND_ABOVE",
    "Block High": "BLOCK_HIGH_AND_ABOVE",
}

SAFETY_CATEGORIES = [
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
]


class GeminiAPI:
    """
    A custom node for ComfyUI that uses the Google Gemini API for text and image generation
    via the official google-generativeai library.
    Includes optional image input (with resizing), system prompt, user instructions,
    thinking mode, and safety settings control.
    """

    CATEGORY = "Creepybits/Beginner's Tools"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "generate_text"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),
                "model": (["gemini-2.5-flash-lite-preview-06-17", "gemini-2.0-flash-lite", "gemini-2.5-pro-preview-06-05", "gemini-2.0-flash", "gemini-2.0-flash-exp"],),
                "max_output_tokens": ("INT", {"default": 1024, "min": 1, "max": 4096}),
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 100}),
            },
            "optional": {
                "user_instructions": ("STRING", {"multiline": True, "default": ""}),
                "api_key_file": ("STRING", {"default": DEFAULT_API_KEY_PATH, "multiline": False}),
                "image": ("IMAGE",),
                "resize_image_to": (["None", "512", "768", "1024"], {"default": "None"}),
                "thinking_mode": (["disable", "enable"], {"default": "disable"}),
                "safety_threshold": (SAFETY_THRESHOLDS, {"default": "Block None"}),
            }
        }


    def generate_text(self, system_prompt, model, max_output_tokens, temperature, top_p, seed, top_k, user_instructions="", api_key_file=None, image=None, resize_image_to="None", thinking_mode="disable", safety_threshold="Block None"):
        """
        Generates text using the Google Gemini API via the google-generativeai library.
        Handles optional image input (with resizing), system prompt, user instructions,
        thinking mode, and safety settings.
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


        # --- Prepare the 'contents' payload for the genai library ---
        combined_prompt_text = ""
        if system_prompt and system_prompt.strip():
             combined_prompt_text += system_prompt.strip() + "\n\n"

        if user_instructions and user_instructions.strip():
             combined_prompt_text += user_instructions.strip()

        contents = []

        if combined_prompt_text or image is None:
            contents.append(combined_prompt_text)


        pil_image = None
        if image is not None:
            try:
                image_data = image.numpy()
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


                # --- Resize Image if specified ---
                if resize_image_to != "None" and pil_image is not None:
                    try:
                         target_size = int(resize_image_to)
                         width, height = pil_image.size
                         if height > width:
                              new_height = target_size
                              new_width = int(width * (target_size / height))
                         else:
                              new_width = target_size
                              new_height = int(height * (target_size / width))

                         new_height = max(1, new_height)
                         new_width = max(1, new_width)

                         pil_image = pil_image.resize((new_width, new_height))
                    except ValueError:
                         pass
                    except Exception:
                         pass

                if pil_image is not None:
                     contents.append(pil_image)


            except Exception as e:
                 return (f"Error: Failed to process image: {e}",)

        if not contents:
             return ("Error: No valid content provided. Ensure system prompt, user instructions, or image are present.",)


        # --- Construct the generationConfig payload ---
        generation_config = {
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            # Note: Seed parameter removed as it caused a 400 error previously.
            # The Gemini API documentation doesn't explicitly mention a seed parameter
            # for this endpoint at the time of writing.
        }

        # --- Add thinkingConfig if thinking_mode is enabled ---
        if thinking_mode == "enable":
             generation_config["thinking_config"] = {"thinking_budget": DEFAULT_THINKING_BUDGET}


        # --- Construct the safety_settings payload ---
        safety_settings = []
        api_threshold = SAFETY_THRESHOLD_MAP.get(safety_threshold, "BLOCK_NONE")

        if api_threshold != "BLOCK_NONE":
            for category_name in SAFETY_CATEGORIES:
                safety_settings.append({
                    "category": category_name,
                    "threshold": api_threshold
                })


        # --- Get the Generative Model ---
        try:
            model_instance = genai.GenerativeModel(model)
        except Exception as e:
            if "Invalid model" in str(e):
                 return (f"Error: Invalid model name '{model}'. Check model availability.",)
            return (f"Error: Could not get Gemini model '{model}'. Check model name, API status, or internet connection: {e}",)


        # --- Send API Request using genai library ---
        try:
            response = model_instance.generate_content(
                contents,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )

            generated_text = ""
            if hasattr(response, 'text'):
                 generated_text = response.text
            elif hasattr(response, 'candidates') and response.candidates:
                 try:
                      if hasattr(response.candidates[0], 'content') and response.candidates[0].content and \
                         hasattr(response.candidates[0].content, 'parts') and response.candidates[0].content.parts:
                          generated_text = response.candidates[0].content.parts[0].text
                 except (AttributeError, IndexError, KeyError):
                      pass


            if not generated_text:
                 if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                     feedback_info = {}
                     if hasattr(response.prompt_feedback, 'block_reason') and response.prompt_feedback.block_reason and hasattr(response.prompt_feedback.block_reason, 'name') and response.prompt_feedback.block_reason.name != 'UNASSIGNED':
                          feedback_info['block_reason'] = response.prompt_feedback.block_reason.name

                     if hasattr(response.prompt_feedback, 'safety_ratings') and response.prompt_feedback.safety_ratings:
                         feedback_info['safety_ratings'] = []
                         for rating in response.prompt_feedback.safety_ratings:
                             if hasattr(rating, 'probability') and hasattr(rating.probability, 'name') and rating.probability.name != 'UNSPECIFIED':
                                 rating_info = {"category": rating.category.name, "probability": rating.probability.name}
                                 feedback_info['safety_ratings'].append(rating_info)

                     if 'block_reason' in feedback_info:
                          return (f"Error: Content generation blocked due to {feedback_info['block_reason']}. Check console for safety feedback.",)
                     elif 'safety_ratings' in feedback_info and feedback_info['safety_ratings']:
                          return ("Error: No text generated. High safety ratings. Check console for details.",)
                     return ("Error: No text generated. API returned empty content/candidates. Check Prompt Feedback in console.",)
                 else:
                      if hasattr(response, 'candidates') and not response.candidates:
                           return ("Error: API returned no candidates (likely blocked). No prompt feedback details available.",)
                      return ("Error: No text generated from the API and no specific feedback provided. Check console.",)


            return (generated_text,)


        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response:
                 if hasattr(e.response, 'text'):
                      try:
                           error_json = json.loads(e.response.text)
                           if 'error' in error_json and 'message' in error_json['error']:
                                api_error_message = error_json['error']['message']
                                error_message = f"API Error: {api_error_message}"
                           elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                      except (json.JSONDecodeError, AttributeError):
                           if hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                           pass

                 elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                      error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"

            return (f"Error: An error occurred during Gemini API call: {error_message}",)


NODE_CLASS_MAPPINGS = {
    "GeminiAPI": GeminiAPI,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiAPI": "Gemini 2.5 Flash/Pro API (Creepybits)",
}

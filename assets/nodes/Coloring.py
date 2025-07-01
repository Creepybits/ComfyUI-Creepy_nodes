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

class Coloring:
    """
    A custom node for ComfyUI that uses the Google Gemini API for text and image generation.
    """

    CATEGORY = "Creepybits/Utilities"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_text"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),                
                "model": (["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-exp-03-25", "gemini-2.0-flash", "gemini-2.0-flash-exp"],),
                "max_output_tokens": ("INT", {"default": 512, "min": 1, "max": 4096}),
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 100}),
            },
            "optional": {
                "api_key_file": ("STRING", {"default": DEFAULT_API_KEY_PATH, "multiline": False}),
                "ref_image": ("IMAGE",),
                "color_image": ("IMAGE",),
                "resize_image_to": (["None", "512", "768", "1024"], {"default": "768"}),
                "thinking_mode": (["disable", "enable"], {"default": "disable"}),
                "safety_threshold": (SAFETY_THRESHOLDS, {"default": "Block None"}),
            }
        }

    def generate_text(self, system_prompt, model, max_output_tokens, temperature, top_p, top_k, api_key_file=None, ref_image=None, color_image=None, resize_image_to="None", thinking_mode="disable", safety_threshold="Block None", **kwargs):
        """Generates text using the Google Gemini API."""
        api_key = os.environ.get("GOOGLE_API_KEY")

        if not api_key and api_key_file and os.path.exists(api_key_file):
            try:
                with open(api_key_file, 'r') as f:
                    api_key = f.read().strip()
            except Exception as e:
                # Keep user-facing warning
                print(f"Warning: Error reading Gemini API key file '{api_key_file}': {e}.")
        elif not api_key and api_key_file and not os.path.exists(api_key_file):
            # Keep user-facing warning
            print(f"Warning: GOOGLE_API_KEY environment variable not set and API key file not found at '{api_key_file}'.")

        if not api_key:
            return ("Error: Gemini API key not found. Please set the GOOGLE_API_KEY environment variable or provide a valid path to an API key file.",)

        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            return (f"Error configuring Gemini API with key: {e}",)

        combined_prompt_text = ""
        if system_prompt and system_prompt.strip():
            combined_prompt_text += system_prompt.strip() + "\n\n"

        contents = []
        
        def process_image(image, image_name="image"): 
            pil_image = None
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
                    print(f"Warning: Unexpected image data shape {image_data.shape}. Attempting conversion to RGB.")
                    try:
                        pil_image = Image.fromarray(image_data).convert('RGB')
                    except Exception as convert_e:                        
                        print(f"Error converting {image_name} format: {convert_e}") 
                        return None 

                return pil_image

            except Exception as e:                
                print(f"Error processing {image_name} for API request: {e}") 
                return None 
        
        processed_ref_image = None
        if ref_image is not None:
            processed_ref_image = process_image(ref_image, "ref_image")
            if processed_ref_image is None:
                return ("Error: Failed to process ref_image",) 

        processed_color_image = None
        if color_image is not None:
            processed_color_image = process_image(color_image, "color_image")
            if processed_color_image is None:
                return ("Error: Failed to process color_image",)  
        
        pil_image = processed_ref_image
        pil_image2 = processed_color_image       
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
            except ValueError:                #
                print(f"Warning: Invalid resize_image_to value '{resize_image_to}'. Skipping resize.")
            except Exception as e:                
                print(f"Error during image resizing: {e}. Skipping resize.")

        if resize_image_to != "None" and pil_image2 is not None:
            try:
                target_size = int(resize_image_to)
                width, height = pil_image2.size
                if height > width:
                    new_height = target_size
                    new_width = int(width * (target_size / height))
                else:
                    new_width = target_size
                    new_height = int(height * (target_size / width))

                new_height = max(1, new_height)
                new_width = max(1, new_width)
               
                pil_image2 = pil_image2.resize((new_width, new_height))
            except ValueError:                
                print(f"Warning: Invalid resize_image_to value '{resize_image_to}'. Skipping resize.")
            except Exception as e:                
                print(f"Error during image resizing: {e}. Skipping resize.")
        
        if pil_image is not None:
            contents.append(pil_image)
        if pil_image2 is not None:
            contents.append(pil_image2)       
        if combined_prompt_text or not contents:
            contents.append(combined_prompt_text)
        
        if not contents:
            return ("Error: No valid content provided. Ensure system prompt, user instructions, or image are present.",)

        generation_config = {
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }

        if thinking_mode == "enable":            
            print(f"Thinking mode enabled with budget {DEFAULT_THINKING_BUDGET}.")

        safety_settings = []
        api_threshold = SAFETY_THRESHOLD_MAP.get(safety_threshold, "BLOCK_NONE")

        if api_threshold != "BLOCK_NONE":            
            print(f"Applying safety threshold '{api_threshold}' to categories: {SAFETY_CATEGORIES}")
        else:            
            print("Safety threshold set to 'Block None'. No safety settings applied.")

        try:
            model_instance = genai.GenerativeModel(model)
        except Exception as e:           
            print(f"Error getting model '{model}': {e}")
            if "Invalid model" in str(e):
                return (f"Error: Invalid model name '{model}'. Check model availability.",)
            return (f"Error: Could not get Gemini model '{model}'. Check model name, API status, or internet connection: {e}",)

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
                    print("Warning: Could not extract text from response.candidates structure.")

            if not generated_text:                
                print("Generated text is empty or extraction failed.")
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:                    
                    print("Prompt Feedback:")
                    feedback_info = {}
                    if hasattr(response.prompt_feedback, 'block_reason') and response.prompt_feedback.block_reason and hasattr(response.prompt_feedback.block_reason.name) and response.prompt_feedback.block_reason.name != 'UNASSIGNED':                        
                        print(f"  Block Reason: {response.prompt_feedback.block_reason.name}")
                        feedback_info['block_reason'] = response.prompt_feedback.block_reason.name

                    if hasattr(response.prompt_feedback, 'safety_ratings') and response.prompt_feedback.safety_ratings:                        
                        print("  Safety Ratings:")
                        feedback_info['safety_ratings'] = []
                        for rating in response.prompt_feedback.safety_ratings:
                            if hasattr(rating, 'probability') and hasattr(rating.probability.name) and rating.probability.name != 'UNSPECIFIED':
                                rating_info = {"category": rating.category.name, "probability": rating.probability.name}                                
                                print(f"    Category: {rating_info['category']}, Probability: {rating_info['probability']}")
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
            print(f"An error occurred during Gemini API call: {e}")
            error_message = str(e)
            if hasattr(e, 'response') and e.response:
                if hasattr(e.response, 'text'):
                    try:
                        error_json = json.loads(e.response.text)
                        if 'error' in error_json and 'message' in error_json['error']:
                            api_error_message = error_json['error']['message']                            
                            print(f"API Error Message from response: {api_error_message}")
                            error_message = f"API Error: {api_error_message}"
                        elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                            error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                    except (json.JSONDecodeError, AttributeError):
                        if hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                            error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"

                elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                    error_message = f"HTTP Error: {e.response.status_code} {e.response.reason}"

            return (f"Error: An error occurred during Gemini API call: {error_message}",)

NODE_CLASS_MAPPINGS = {
    "Coloring": Coloring,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Coloring": "Coloring Node (Creepybits)",
}

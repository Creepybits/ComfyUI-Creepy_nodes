import os
import json
from google import genai
from google.genai import types
from PIL import Image
import torch
import numpy as np

# Path to your central API key config
API_CONFIG_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\api_keys_config.json"
DEFAULT_THINKING_BUDGET = 4096

SAFETY_THRESHOLD_MAP = {
    "Block None": "BLOCK_NONE",
    "Block Low": "BLOCK_LOW_AND_ABOVE",
    "Block Medium": "BLOCK_MEDIUM_AND_ABOVE",
    "Block High": "BLOCK_HIGH_AND_ABOVE",
}

def get_api_key_list():
    if os.path.exists(API_CONFIG_PATH):
        try:
            with open(API_CONFIG_PATH, 'r') as f:
                config = json.load(f)
                return list(config.keys())
        except Exception:
            return ["Error loading JSON"]
    return ["Config not found"]

class GeminiAPICreepybits:
    CATEGORY = "Creepybits/API"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_text"

    @classmethod
    def INPUT_TYPES(s):
        key_list = get_api_key_list()
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),
                "model": (["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-flash-lite-preview-09-2025", "gemini-2.5-flash-preview-09-2025", "gemini-2.0-flash-exp"],),
                "max_output_tokens": ("INT", {"default": 1024, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 100}),
                "api_key_selection": (key_list,),
            },
            "optional": {
                "user_instructions": ("STRING", {"multiline": True, "default": ""}),
                "image": ("IMAGE",),
                "resize_image_to": (["None", "512", "768", "1024"], {"default": "None"}),
                "thinking_mode": (["disable", "enable"], {"default": "disable"}),
                "safety_threshold": (list(SAFETY_THRESHOLD_MAP.keys()), {"default": "Block None"}),
            }
        }

    def generate_text(self, system_prompt, model, max_output_tokens, temperature, top_p, seed, top_k,
                      api_key_selection, user_instructions="", image=None, resize_image_to="None",
                      thinking_mode="disable", safety_threshold="Block None"):

        # --- API Key Extraction ---
        api_key = None
        if os.path.exists(API_CONFIG_PATH):
            try:
                with open(API_CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                    key_file_path = config.get(api_key_selection)
                    if key_file_path and os.path.exists(key_file_path):
                        with open(key_file_path, 'r') as kf:
                            api_key = kf.read().strip()
            except Exception as e:
                return (f"Error reading key config: {e}",)

        if not api_key: return ("Error: API key not found.",)

        try:
            client = genai.Client(api_key=api_key)
        except Exception as e: return (f"Error initializing Client: {e}",)

        # Prepare Content
        contents = []
        if user_instructions and user_instructions.strip():
            contents.append(user_instructions.strip())

        if image is not None:
            try:
                i = 255. * image[0].cpu().numpy()
                img = Image.fromarray(np.uint8(i))
                if resize_image_to != "None":
                    target_size = int(resize_image_to)
                    img.thumbnail((target_size, target_size), Image.LANCZOS)
                contents.append(img)
            except Exception as e: return (f"Error processing image: {e}",)

        # --- THE FIX: Fallback for Text-Only Mode ---
        if not contents:
            if system_prompt and system_prompt.strip():
                # If only system prompt is provided, we send a generic trigger message
                contents.append("Please respond based on your system instructions.")
            else:
                return ("Error: No input provided (need system prompt, instructions, or image).",)

        # Build Config
        safety_settings = [
            types.SafetySetting(category=cat, threshold=SAFETY_THRESHOLD_MAP[safety_threshold])
            for cat in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
                        "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
        ]

        generate_config = {
            "system_instruction": system_prompt if system_prompt.strip() else None,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "safety_settings": safety_settings,
        }

        if thinking_mode == "enable":
            generate_config["thinking_config"] = {"include_thoughts": True}

        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(**generate_config)
            )
            return (response.text,)
        except Exception as e:
            return (f"API Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {"GeminiAPICreepybits": GeminiAPICreepybits}
NODE_DISPLAY_NAME_MAPPINGS = {"GeminiAPICreepybits": "Gemini 2.5 Unified API (Creepybits)"}

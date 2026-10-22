from PIL import Image
import numpy as np

from .libs.gemini_common import GEMINI_MODELS, SAFETY_THRESHOLD_MAP, get_api_key_list, build_config, generate


class GeminiAPICreepybits:
    CATEGORY = "Creepybits/API"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_text"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),
                "model": (GEMINI_MODELS,),
                "max_output_tokens": ("INT", {"default": 1024, "min": 1, "max": 65536}),
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 100}),
                "api_key_selection": (get_api_key_list(),),
            },
            "optional": {
                "user_instructions": ("STRING", {"multiline": True, "default": ""}),
                "image": ("IMAGE",),
                "resize_image_to": (["None", "512", "768", "1024"], {"default": "None"}),
                "thinking_mode": (["disable", "enable"], {"default": "disable"}),
                "safety_threshold": (list(SAFETY_THRESHOLD_MAP.keys()), {"default": "Block None"}),
                "custom_model": ("STRING", {"default": "", "tooltip": "Overrides the model dropdown, e.g. for newly released Gemini models."}),
            }
        }

    def generate_text(self, system_prompt, model, max_output_tokens, temperature, top_p, seed, top_k,
                      api_key_selection, user_instructions="", image=None, resize_image_to="None",
                      thinking_mode="disable", safety_threshold="Block None", custom_model=""):
        model = custom_model.strip() or model

        contents = []
        if user_instructions and user_instructions.strip():
            contents.append(user_instructions.strip())

        if image is not None:
            try:
                img = Image.fromarray(np.clip(255. * image[0].cpu().numpy(), 0, 255).astype(np.uint8))
                if resize_image_to != "None":
                    target_size = int(resize_image_to)
                    img.thumbnail((target_size, target_size), Image.LANCZOS)
                contents.append(img)
            except Exception as e:
                return (f"Error processing image: {e}",)

        # Gemini needs at least one user message, even when everything is in the system prompt.
        if not contents:
            if system_prompt and system_prompt.strip():
                contents.append("Please respond based on your system instructions.")
            else:
                return ("Error: No input provided (need system prompt, instructions, or image).",)

        config = build_config(system_prompt, model, thinking_mode, safety_threshold,
                              temperature=temperature, top_p=top_p, top_k=top_k,
                              max_output_tokens=max_output_tokens, seed=seed % 2**31)  # API takes an int32 seed
        return (generate(api_key_selection, model, contents, config),)


NODE_CLASS_MAPPINGS = {"GeminiAPICreepybits": GeminiAPICreepybits}
NODE_DISPLAY_NAME_MAPPINGS = {"GeminiAPICreepybits": "Gemini Unified API (Creepybits)"}

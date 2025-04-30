import os
import sys
import comfy.sd
import comfy.utils
import re

class PromptGenerator:

    def __init__(self):
        # Get the directory of the current script (SystemPromp.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the text file: up one level, then into "assets/prompts"
        assets_dir = os.path.dirname(script_dir) # go up to assets
        filepath = os.path.join(assets_dir, "prompts", "prompt.txt")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.fixed_text = f.read()
        except FileNotFoundError:
            print(f"Error: system_prompt.txt not found at {filepath}")
            self.fixed_text = "ERROR: Prompt file not found."  # Provide a fallback
        except Exception as e:
            print(f"Error reading system_prompt.txt: {e}")
            self.fixed_text = "ERROR: Could not read prompt file."  # Provide a fallback

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_2": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "concat_texts"

    CATEGORY = "Creepybits/Prompt"

    def concat_texts(self, text_2):
        combined_text = self.fixed_text + text_2
        return (combined_text,)


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "PromptGenerator": PromptGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "PromptGenerator": "Prompt Generator (Creepybits)",
}

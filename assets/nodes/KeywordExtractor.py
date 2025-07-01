import os
import sys
import comfy.sd
import comfy.utils
import re

class KeywordExtractor:

    def __init__(self):       
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        assets_dir = os.path.dirname(script_dir) 
        filepath = os.path.join(assets_dir, "prompts", "keywords.txt")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.fixed_text = f.read()
        except FileNotFoundError:
            print(f"Error: system_prompt.txt not found at {filepath}")
            self.fixed_text = "ERROR: Prompt file not found."  
        except Exception as e:
            print(f"Error reading system_prompt.txt: {e}")
            self.fixed_text = "ERROR: Could not read prompt file."  

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


NODE_CLASS_MAPPINGS = {  
      "KeywordExtractor": KeywordExtractor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "KeywordExtractor": "Keyword Extractor (Creepybits)",
}

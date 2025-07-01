import os
import json
import folder_paths 

class Categorizer:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.dirname(self.script_dir)
        self.prompts_dir = os.path.join(self.assets_dir, "prompts")
        self.json_file = "categorizer.json"

        try:
            with open(os.path.join(self.assets_dir, self.json_file), "r", encoding="utf-8") as f:
                data = json.load(f)
                self.prompt_files = data.get("prompts", []) 
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            self.prompt_files = []
        except Exception:
            
            self.prompt_files = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_file": (cls.get_prompt_file_names(),),
            },
            "optional": {
                "optional_input": ("*",)
            }
        }

    @classmethod
    def get_prompt_file_names(cls):        
        if not hasattr(cls, '_prompt_files'):
            cls._prompt_files = Categorizer().prompt_files
        return cls._prompt_files

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "load_prompt"
    CATEGORY = "Creepybits/Utilities"

    def load_prompt(self, prompt_file, optional_input=None):
        filepath = os.path.join(self.prompts_dir, prompt_file)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                prompt_text = f.read()
            return (prompt_text,)
        except FileNotFoundError:            
            error_message = "ERROR: Prompt file not found."
            return (error_message,)
        except Exception as e:            
            error_message = f"ERROR: Could not read prompt file: {e}"
            return (error_message,)

NODE_CLASS_MAPPINGS = {
      "Categorizer": Categorizer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "Categorizer": "Categorizer (Creepybits)",
}

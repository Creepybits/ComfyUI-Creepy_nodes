import os
import json
import folder_paths

class Categorizer:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.dirname(self.script_dir)  # Go up one directory level
        self.prompts_dir = os.path.join(self.assets_dir, "prompts")  # Correct prompts dir as well
        self.json_file = "categorizer.json"  # New json file

        try:
            with open(os.path.join(self.assets_dir, self.json_file), "r", encoding="utf-8") as f:
                data = json.load(f)
                self.prompt_files = data["prompts"]  # Load the prompt_files
        except FileNotFoundError as e:
            print(f"File not found error: {e}")
            self.prompt_files = []
        except KeyError as e:
            print(f"Key error: {e}")
            self.prompt_files = []
        except json.JSONDecodeError as e:
            print(f"Json decode error: {e}")
            self.prompt_files = []
        except Exception as e:
            print(f"Other error {e}")
            self.prompt_files = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_file": (cls.get_prompt_file_names(),),
            },
            "optional": {
                "optional_input": ("*",)  # This is added because ALL nodes has to have an input.
            }
        }

    @classmethod
    def get_prompt_file_names(cls):
        # Access the prompt_files from the class itself
        # This ensures that it's only loaded once
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
            print(f"load_prompt: Returning (success): Type={type(prompt_text)}, Value={prompt_text}")
            return (prompt_text,)
        except FileNotFoundError:
            error_message = "ERROR: Prompt file not found."
            print(f"load_prompt: Returning (FileNotFoundError): Type={type(error_message)}, Value={error_message}")  # Add this
            return (error_message,)
        except Exception as e:
            error_message = f"ERROR: Could not read prompt file: {e}"
            print(f"load_prompt: Returning (Exception): Type={type(error_message)}, Value={error_message}")  # Add this
            return (error_message,)


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "Categorizer": Categorizer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "Categorizer": "Categorizer (Creepybits)",
}

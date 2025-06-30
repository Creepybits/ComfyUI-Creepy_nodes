import os
import json
import folder_paths # While not directly used in the final logic, it's a common ComfyUI import, keep for consistency if desired.

class Categorizer:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.dirname(self.script_dir)
        self.prompts_dir = os.path.join(self.assets_dir, "prompts")
        self.json_file = "categorizer.json"

        try:
            with open(os.path.join(self.assets_dir, self.json_file), "r", encoding="utf-8") as f:
                data = json.load(f)
                self.prompt_files = data.get("prompts", []) # Use .get() with a default for robustness
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            # Log these errors internally if needed by ComfyUI's logging system,
            # but avoid print statements in production nodes for general users.
            # For now, we'll just ensure prompt_files is empty.
            self.prompt_files = []
        except Exception:
            # Catch any other unexpected errors during file loading
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
        # Load prompt files only once per class instance to populate the dropdown
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
            # ComfyUI often handles node errors gracefully in the UI/console
            # without needing a print statement directly from the node's function.
            # Returning an error message string is a good fallback for the user.
            error_message = "ERROR: Prompt file not found."
            return (error_message,)
        except Exception as e:
            # Catch any other unexpected errors during file reading
            error_message = f"ERROR: Could not read prompt file: {e}"
            return (error_message,)

NODE_CLASS_MAPPINGS = {
      "Categorizer": Categorizer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "Categorizer": "Categorizer (Creepybits)",
}

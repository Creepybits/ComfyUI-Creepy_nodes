import os
import json

class SummaryWriter:
    """
    A ComfyUI node that loads text from a selected prompt file
    and combines it with user-provided text.
    """

    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.dirname(script_dir)
        self.prompts_dir = os.path.join(self.assets_dir, "prompts")
        self.json_file = "summary.json"
        self.json_filepath = os.path.join(self.assets_dir, self.json_file)

        try:
            with open(self.json_filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.prompt_files = data.get("prompts", [])
        except FileNotFoundError:
            print(f"Error: {self.json_file} not found at {self.json_filepath}")
            self.prompt_files = ["ERROR: JSON file not found."]
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error reading {self.json_file}: {e}")
            self.prompt_files = ["ERROR: Invalid JSON format."]
        except KeyError:
             print(f"KeyError: 'prompts' key not found in {self.json_file}")
             self.prompt_files = ["ERROR: 'prompts' key missing in JSON."]
        except Exception as e:
            print(f"Other error reading {self.json_file}: {e}")
            self.prompt_files = [f"ERROR: Could not read JSON file: {e}"]


    @classmethod
    def INPUT_TYPES(cls):
        prompt_file_names = cls.get_prompt_file_names()
        if not prompt_file_names:
            prompt_file_names = ["ERROR: Could not load prompt list."]

        return {
            "required": {
                "prompt_file": (prompt_file_names,),
                "text_to_combine": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    @classmethod
    def get_prompt_file_names(cls):
        if not hasattr(cls, '_prompt_files'):
            temp_instance = cls()
            cls._prompt_files = temp_instance.prompt_files
        return cls._prompt_files

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_text",)

    FUNCTION = "combine_text_from_file_and_input"

    CATEGORY = "Creepybits/Prompt"

    def combine_text_from_file_and_input(self, prompt_file, text_to_combine):
        filepath = os.path.join(self.prompts_dir, prompt_file)
        file_text = ""

        if not prompt_file.startswith("ERROR:"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    file_text = f.read()
            except FileNotFoundError:
                error_message = f"ERROR: Prompt file not found: {filepath}"
                print(error_message)
                return (error_message,)
            except Exception as e:
                error_message = f"ERROR: Could not read prompt file {filepath}: {e}"
                print(error_message)
                return (error_message,)
        else:
             return (prompt_file,)

        combined_text = file_text + "\n\n" + text_to_combine

        return (combined_text,)


NODE_CLASS_MAPPINGS = {
      "SummaryWriter": SummaryWriter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "SummaryWriter": "Summary Writer (Creepybits)",
}

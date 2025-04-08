import os
import json
import folder_paths

class PeopleEvaluationNode:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.dirname(self.script_dir) #Go up one directory level
        self.prompts_dir = os.path.join(self.assets_dir, "prompts")
        self.json_file = "evaluate_people.json"  # New json file
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
                "prompt_file": (PeopleEvaluationNode.get_prompt_file_names(),),
            },
            "optional": {
                "optional_input": ("*",)  # This is added because ALL nodes has to have an input.
            }
        }

    @classmethod
    def get_prompt_file_names(cls):
        #Create a new instance of the PeopleEvaluationNode
        instance = PeopleEvaluationNode()
        # Return the prompt_files
        return instance.prompt_files

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "load_prompt"
    CATEGORY = "Creepybits/Prompt"

    def load_prompt(self, prompt_file, optional_input=None):
        filepath = os.path.join(self.assets_dir, "prompts", prompt_file)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                prompt_text = f.read()
            print(f"load_prompt: Returning (success): Type={type(prompt_text)}, Value={prompt_text}")
            return (prompt_text,)
        except FileNotFoundError:
            return "ERROR: Prompt file not found."
        except Exception as e:
            return f"ERROR: Could not read prompt file: {e}"

NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
    "PeopleEvaluationNode": PeopleEvaluationNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PeopleEvaluationNode": "People Evaluation Node (Creepybits)",
}

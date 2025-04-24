# --- START OF FILE SummaryWriter.py ---

import os
import json
import folder_paths # Keep folder_paths if needed for other things, but not strictly for this file path logic

class SummaryWriter:
    """
    A ComfyUI node that loads text from a selected prompt file
    and combines it with user-provided text.
    """

    def __init__(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the assets directory (up one level)
        self.assets_dir = os.path.dirname(script_dir)

        # Construct the full path to the prompts directory
        self.prompts_dir = os.path.join(self.assets_dir, "prompts")

        # Define the JSON file name
        self.json_file = "summary.json" # Assuming summary.json is directly in the assets folder

        # Path to the JSON file containing prompt list
        self.json_filepath = os.path.join(self.assets_dir, self.json_file)


        try:
            # Load the list of prompt filenames from the JSON file
            with open(self.json_filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Assuming the JSON structure is {"prompts": ["file1.txt", "file2.txt", ...]}
                self.prompt_files = data.get("prompts", []) # Use .get to handle missing key
        except FileNotFoundError:
            print(f"Error: {self.json_file} not found at {self.json_filepath}")
            self.prompt_files = ["ERROR: JSON file not found."] # Provide a fallback for dropdown
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error reading {self.json_file}: {e}")
            self.prompt_files = ["ERROR: Invalid JSON format."] # Provide a fallback for dropdown
        except KeyError:
             print(f"KeyError: 'prompts' key not found in {self.json_file}")
             self.prompt_files = ["ERROR: 'prompts' key missing in JSON."] # Provide a fallback for dropdown
        except Exception as e:
            print(f"Other error reading {self.json_file}: {e}")
            self.prompt_files = [f"ERROR: Could not read JSON file: {e}"] # Provide a fallback for dropdown


    @classmethod
    def INPUT_TYPES(cls):
        # Load prompt file names using the class method
        prompt_file_names = cls.get_prompt_file_names()
        if not prompt_file_names:
            # If loading failed in __init__, provide a default error option
            prompt_file_names = ["ERROR: Could not load prompt list."]

        return {
            "required": {
                "prompt_file": (prompt_file_names,), # Dropdown populated from JSON
                "text_to_combine": ("STRING", {"multiline": True, "default": ""}), # New input for user text
            },
            # Removed "optional_input": ("*",) as it's no longer necessary with required inputs
        }

    @classmethod
    def get_prompt_file_names(cls):
        # This class method is used by INPUT_TYPES to get the list for the dropdown.
        # It ensures the prompt_files list is loaded, ideally only once.
        if not hasattr(cls, '_prompt_files'):
            # Create a temporary instance just to run __init__ and load the files list
            temp_instance = cls()
            cls._prompt_files = temp_instance.prompt_files
        return cls._prompt_files

    RETURN_TYPES = ("STRING",) # Outputs a single string
    RETURN_NAMES = ("combined_text",) # Name of the output

    FUNCTION = "combine_text_from_file_and_input" # New function name

    CATEGORY = "Creepybits/Prompt" # Node category in ComfyUI

    def combine_text_from_file_and_input(self, prompt_file, text_to_combine):
        """
        Loads text from the selected prompt file and combines it with the provided text input.
        """
        filepath = os.path.join(self.prompts_dir, prompt_file)
        file_text = "" # Initialize file text

        # --- Load text from the selected file ---
        # Only try to load if the selected prompt_file is not an error message
        if not prompt_file.startswith("ERROR:"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    file_text = f.read()
            except FileNotFoundError:
                error_message = f"ERROR: Prompt file not found: {filepath}"
                print(error_message)
                return (error_message,) # Return error message as output
            except Exception as e:
                error_message = f"ERROR: Could not read prompt file {filepath}: {e}"
                print(error_message)
                return (error_message,) # Return error message as output
        else:
             # If prompt_file is an error message itself (from JSON loading failure)
             return (prompt_file,)


        # --- Combine the loaded text and the user input ---
        # You can customize how they are combined. Adding a newline is common.
        combined_text = file_text + "\n\n" + text_to_combine

        # --- Return the combined text ---
        # print(f"Combined text output: {combined_text}") # Optional: for debugging
        return (combined_text,)


# --- ComfyUI Node Mappings ---
NODE_CLASS_MAPPINGS = {
      "SummaryWriter": SummaryWriter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "SummaryWriter": "Summary Writer (Creepybits)", # Node name in ComfyUI interface
}

# --- END OF FILE SummaryWriter.py ---

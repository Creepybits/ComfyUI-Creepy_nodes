import os
import json

class WorldWeaverPrompt:
    """
    A dedicated ComfyUI node that internally loads the specific
    World Weaver system prompt and combines it with user-provided text.
    This is a "black box" node with no file selection.
    """

    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.dirname(script_dir)
        self.prompts_dir = os.path.join(assets_dir, "prompts")

        # --- HARDCODED FILENAME ---
        # The specific prompt file is now hardcoded.
        # Change this if your filename is different.
        self.prompt_file = "Scene_Director.txt" 

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # The dropdown is gone. We only need the user's input text.
                "user_text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_text",)

    FUNCTION = "combine_world_weaver_prompt"

    CATEGORY = "Creepybits/Prompt"

    def combine_world_weaver_prompt(self, user_text):
        # The filename is now taken from self.prompt_file, not a user input.
        filepath = os.path.join(self.prompts_dir, self.prompt_file)
        file_text = ""

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                file_text = f.read()
        except FileNotFoundError:
            error_message = f"ERROR: World Weaver prompt file not found at: {filepath}"
            print(error_message)
            return (error_message,)
        except Exception as e:
            error_message = f"ERROR: Could not read World Weaver prompt file {filepath}: {e}"
            print(error_message)
            return (error_message,)

        # Combine the internal system prompt with the user's text.
        combined_text = file_text + "\n\n" + user_text

        return (combined_text,)


NODE_CLASS_MAPPINGS = {
      "WorldWeaverPrompt": WorldWeaverPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "WorldWeaverPrompt": "World Weaver Prompt (Creepybits)",
}

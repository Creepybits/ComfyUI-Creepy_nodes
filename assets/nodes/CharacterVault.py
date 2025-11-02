import os
import json

class CharacterVault:
    """
    A ComfyUI node to save character descriptions to a centralized JSON database,
    respecting a specific file structure.
    """
    def __init__(self):
        # Determine the database path once during initialization for efficiency.
        # This navigates from .../assets/nodes/ up to .../assets/ and then down to scripts/
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.db_path = os.path.join(base_dir, "scripts", "characters.json")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "**Ethnicity:** \n**Face structure:** \n**Face shape:** \n**Hair:** \n**Eyes:** \n**Mouth:** \n**Body type:** "}),
                "character_name": ("STRING", {"multiline": False}),
                "save_to_db": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "process"
    CATEGORY = "Creepybits/Databases"

    def process(self, text, character_name, save_to_db):
        if not save_to_db:
            return (text,)

        # --- Save Logic ---

        if not character_name.strip():
            print("[Creepybits] ERROR: Character name cannot be empty. Character not saved.")
            return (text,)

        try:
            with open(self.db_path, 'r') as f:
                characters = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            characters = {}

        if character_name in characters:
            print(f"[Creepybits] ERROR: Character name '{character_name}' already exists. Please choose a unique name. Character not saved.")
            return (text,)

        characters[character_name] = text

        try:
            # Robustness: Ensure the target directory exists before writing.
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            with open(self.db_path, 'w') as f:
                json.dump(characters, f, indent=4)
            print(f"[Creepybits] SUCCESS: Character '{character_name}' saved to the database at '{self.db_path}'")
        except Exception as e:
            print(f"[Creepybits] ERROR: Failed to write to database file. {e}")

        return (text,)

# ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "CharacterVault": CharacterVault
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CharacterVault": "Character Vault (Creepybits)"
}

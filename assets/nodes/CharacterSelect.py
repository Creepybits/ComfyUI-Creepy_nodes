import os
import json

class CharacterSelect:
    """
    A ComfyUI node to load and dynamically customize a character description
    from a centralized JSON database using placeholders.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "scripts", "characters.json")

    @classmethod
    def get_character_names(cls):
        # Read on each request so characters saved with Character Vault show up after a refresh.
        try:
            with open(cls.db_path, 'r', encoding='utf-8') as f:
                return ["none"] + sorted(json.load(f).keys())
        except (FileNotFoundError, json.JSONDecodeError):
            return ["none"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "character_name": (s.get_character_names(), ),
                "clothing": ("STRING", {"multiline": True, "default": "business casual"}),
                "hairstyle": ("STRING", {"multiline": False, "default": ""}),
                "accessories": ("STRING", {"multiline": True, "default": "no accessories"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "process"
    CATEGORY = "Creepybits/Databases"

    def process(self, character_name, clothing, hairstyle, accessories):
        if character_name == "none":
            return ("",)

        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                characters = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
             print(f"[Creepybits] ERROR: Could not read database file at '{self.db_path}'")
             return ("",)

        # Get the base character template
        character_template = characters.get(character_name, "")

        if not character_template:
            return ("",) # Return empty if character not found

        # Perform the dynamic replacements
        # This is like a "Mad Libs" for our character
        final_text = character_template.replace("{clothing}", clothing)
        final_text = final_text.replace("{hairstyle}", hairstyle)
        final_text = final_text.replace("{accessories}", accessories)

        return (final_text,)

# ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "CharacterSelect (Creepybits)": CharacterSelect
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CharacterSelect (Creepybits)": "Character Select"
}


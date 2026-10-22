from .libs.prompt_utils import read_prompt, prompt_mtime


class WorldWeaverPrompt:
    """
    A dedicated ComfyUI node that internally loads the specific
    World Weaver system prompt and combines it with user-provided text.
    This is a "black box" node with no file selection.
    """

    # Change this if your filename is different.
    PROMPT_FILE = "Scene_Director.txt"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_text",)

    FUNCTION = "combine_world_weaver_prompt"

    CATEGORY = "Creepybits/Prompt"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return prompt_mtime(cls.PROMPT_FILE)

    def combine_world_weaver_prompt(self, user_text):
        file_text = read_prompt(self.PROMPT_FILE)
        if file_text.startswith("ERROR:"):
            return (file_text,)

        # Combine the internal system prompt with the user's text.
        return (file_text + "\n\n" + user_text,)


NODE_CLASS_MAPPINGS = {
      "WorldWeaverPrompt": WorldWeaverPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "WorldWeaverPrompt": "World Weaver Prompt (Creepybits)",
}

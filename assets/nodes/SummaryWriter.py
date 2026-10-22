from .libs.prompt_utils import load_prompt_list, read_prompt, prompt_mtime


class SummaryWriter:
    """
    A ComfyUI node that loads text from a selected prompt file
    and combines it with user-provided text.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_file": (load_prompt_list("summary.json"),),
                "text_to_combine": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_text",)

    FUNCTION = "combine_text_from_file_and_input"

    CATEGORY = "Creepybits/Prompt"

    @classmethod
    def IS_CHANGED(cls, prompt_file, **kwargs):
        return prompt_mtime(prompt_file)

    def combine_text_from_file_and_input(self, prompt_file, text_to_combine):
        if prompt_file.startswith("ERROR:"):
            return (prompt_file,)

        file_text = read_prompt(prompt_file)
        if file_text.startswith("ERROR:"):
            return (file_text,)

        return (file_text + "\n\n" + text_to_combine,)


NODE_CLASS_MAPPINGS = {
      "SummaryWriter": SummaryWriter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "SummaryWriter": "Summary Writer (Creepybits)",
}

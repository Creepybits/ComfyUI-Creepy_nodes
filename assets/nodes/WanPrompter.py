from .libs.prompt_utils import FixedPromptNode


class WanPrompter(FixedPromptNode):
    PROMPT_FILE = "wan_prompt.txt"


NODE_CLASS_MAPPINGS = {
      "WanPrompter": WanPrompter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "WanPrompter": "WAN Prompter (Creepybits)",
}

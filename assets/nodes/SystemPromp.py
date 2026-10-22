from .libs.prompt_utils import FixedPromptNode


class SystemPrompt(FixedPromptNode):
    PROMPT_FILE = "system_prompt.txt"


NODE_CLASS_MAPPINGS = {
      "SystemPromp": SystemPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "SystemPromp": "System Prompt (Creepybits)",
}

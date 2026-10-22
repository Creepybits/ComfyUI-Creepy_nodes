from .libs.prompt_utils import FixedPromptNode


class QWENPrompt(FixedPromptNode):
    PROMPT_FILE = "QWEN_prompt.md"


NODE_CLASS_MAPPINGS = {
      "QWENPrompt": QWENPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "QWENPrompt": "QWEN Prompter (Creepybits)",
}

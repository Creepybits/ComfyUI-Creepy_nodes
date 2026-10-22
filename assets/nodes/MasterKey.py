from .libs.prompt_utils import FixedPromptNode


class MasterKey(FixedPromptNode):
    PROMPT_FILE = "prompt.txt"


NODE_CLASS_MAPPINGS = {
      "MasterKey": MasterKey,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "MasterKey": "Master Key (Creepybits)",
}

from .libs.prompt_utils import PromptListNode


class Categorizer(PromptListNode):
    PROMPT_LIST_FILE = "categorizer.json"
    CATEGORY = "Creepybits/Utilities"


NODE_CLASS_MAPPINGS = {
      "Categorizer": Categorizer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "Categorizer": "Categorizer (Creepybits)",
}

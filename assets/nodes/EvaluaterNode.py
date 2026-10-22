from .libs.prompt_utils import PromptListNode


class EvaluaterNode(PromptListNode):
    PROMPT_LIST_FILE = "evaluate_img.json"


NODE_CLASS_MAPPINGS = {
      "EvaluaterNode": EvaluaterNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "EvaluaterNode": "Evaluater Node (Creepybits)",
}

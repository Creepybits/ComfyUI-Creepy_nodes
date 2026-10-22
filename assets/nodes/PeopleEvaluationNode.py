from .libs.prompt_utils import PromptListNode


class PeopleEvaluationNode(PromptListNode):
    PROMPT_LIST_FILE = "evaluate_people.json"


NODE_CLASS_MAPPINGS = {
      "PeopleEvaluationNode": PeopleEvaluationNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "PeopleEvaluationNode": "People Evaluation Node (Creepybits)",
}

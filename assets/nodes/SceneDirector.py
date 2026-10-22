from .libs.prompt_utils import FixedPromptNode


class SceneDirector(FixedPromptNode):
    PROMPT_FILE = "Scene_Director.md"


NODE_CLASS_MAPPINGS = {
      "SceneDirector": SceneDirector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "SceneDirector": "Scene Director (Creepybits)",
}

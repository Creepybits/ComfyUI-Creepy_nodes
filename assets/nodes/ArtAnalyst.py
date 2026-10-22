from .libs.prompt_utils import FixedPromptNode


class ArtAnalyst(FixedPromptNode):
    PROMPT_FILE = "face_detail.md"


NODE_CLASS_MAPPINGS = {
      "ArtAnalyst": ArtAnalyst,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "ArtAnalyst": "Art Analyst (Creepybits)",
}

from .libs.prompt_utils import FixedPromptNode


class KeywordExtractor(FixedPromptNode):
    PROMPT_FILE = "keywords.txt"


NODE_CLASS_MAPPINGS = {
      "KeywordExtractor": KeywordExtractor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "KeywordExtractor": "Keyword Extractor (Creepybits)",
}

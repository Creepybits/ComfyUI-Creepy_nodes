from .libs.prompt_utils import FixedPromptNode


class AudioKeywordExtractor(FixedPromptNode):
    PROMPT_FILE = "audio_keywords.txt"
    CATEGORY = "Creepybits/Audio"


NODE_CLASS_MAPPINGS = {
      "AudioKeywordExtractor": AudioKeywordExtractor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "AudioKeywordExtractor": "Audio To Image Draft (Creepybits)",
}

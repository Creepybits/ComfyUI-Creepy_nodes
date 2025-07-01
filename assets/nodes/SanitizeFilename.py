import re

class SanitizeFilename:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("sanitized_text",)
    FUNCTION = "sanitize"
    CATEGORY = "Creepybits/Utilities"

    def sanitize(self, text):
        
        text = text.replace('\n', '')        
        text = re.sub(r'[\\/*?:"<>|]', "", text)          
        text = text.strip()
        return (text,)


NODE_CLASS_MAPPINGS = { 
      "SanitizeFilename": SanitizeFilename,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "SanitizeFilename": "Sanitize Filename (Creepybits)",
}

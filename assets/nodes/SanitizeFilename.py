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
    CATEGORY = "Utilities"

    def sanitize(self, text):
        """
        Sanitizes a filename by removing or replacing invalid characters.

        Args:
            text (str): The text to sanitize.

        Returns:
            str: The sanitized text.
        """
        # Replace newline characters with an empty string
        text = text.replace('\n', '')
        # Replace or remove other invalid characters (example)
        text = re.sub(r'[\\/*?:"<>|]', "", text)  # Remove invalid characters
        # Remove leading/trailing whitespace
        text = text.strip()
        return (text,)


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "SanitizeFilename": SanitizeFilename,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "SanitizeFilename": "Sanitize Filename (Creepybits)",
}

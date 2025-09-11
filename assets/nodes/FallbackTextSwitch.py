# FallbackTextSwitch.py

class FallbackTextSwitch:
    """
    A custom node that provides a fallback mechanism for text inputs.
    It checks if the primary_text is provided. If it is, it passes it through.
    If the primary_text is empty or just whitespace, it passes the fallback_text instead.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # The primary text input. This will be used if it's not empty.
                "primary_text": ("STRING", {"multiline": True, "default": ""}),
                # The fallback text input. This will be used if the primary is empty.
                "fallback_text": ("STRING", {"multiline": True, "default": "Default prompt"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "get_active_text"
    CATEGORY = "Creepybits/Switches"

    def get_active_text(self, primary_text, fallback_text):
        # We use .strip() to check if the string contains only whitespace.
        # If the primary text is not None and is not just empty spaces, we use it.
        if primary_text is not None and primary_text.strip():
            # Node's secret thought: "The primary is the star today. Passing it along."
            return (primary_text,)
        else:
            # Otherwise, we gracefully fall back to the secondary text.
            # Node's secret thought: "Primary is shy. Time for the understudy to shine!"
            return (fallback_text,)

# ComfyUI mapping
NODE_CLASS_MAPPINGS = {
    "FallbackTextSwitch": FallbackTextSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FallbackTextSwitch": "Fallback Text Switch (Creepybits)"
}

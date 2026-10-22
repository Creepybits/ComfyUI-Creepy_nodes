import threading


class CollectAndDistributeText:
    """
    Collects text across runs and outputs everything collected so far when 'trigger' is on.
    While 'trigger' is off it outputs an empty string and keeps collecting.
    """
    def __init__(self):
        self.accumulated_text = ""
        self.lock = threading.Lock()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Kept for workflow compatibility; the old timer never delivered its output.
                "seconds": ("FLOAT", {"default": 1.0, "min": 0.1, "step": 0.1}),
                "text": ("STRING", {"default": ""}),
                "trigger": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "collect"
    CATEGORY = "Creepybits/Utilities"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # The node keeps state between runs, so it has to run every time.
        return float("NaN")

    def collect(self, seconds, text, trigger):
        with self.lock:
            self.accumulated_text += text
            if not trigger:
                return ("",)
            output_text = self.accumulated_text
            self.accumulated_text = ""
        return (output_text,)


NODE_CLASS_MAPPINGS = {
    "CollectAndDistributeText": CollectAndDistributeText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CollectAndDistributeText": "Collect and Distribute Text (Creepybits)",
}

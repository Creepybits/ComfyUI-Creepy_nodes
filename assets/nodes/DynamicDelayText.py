import time
import threading

class DynamicDelayText:
    def __init__(self):
        self.timer = None
        self.lock = threading.Lock()  # Ensure thread safety
        self.output_text = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seconds": ("FLOAT", {"default": 1.0, "min": 0.1, "step": 0.1}),
                "text": ("STRING",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "delay"
    CATEGORY = "Creepybits/Utilities"

    def delay(self, seconds, text):
        with self.lock:  # Thread-safe access to shared resources
            self.output_text = text  # Store the text for output
            if self.timer is not None:
                self.timer.cancel()  # Cancel any existing timer
            self.timer = threading.Timer(seconds, self.output)  # Start a new timer
            self.timer.start()
        return ("",)  # Return empty string immediately

    def output(self):
        with self.lock:  # Thread-safe access to shared resources
            text_to_output = self.output_text
            self.output_text = ""
            self.timer = None  # Clear the timer
        return (text_to_output,)

NODE_CLASS_MAPPINGS = {
    "DynamicDelayText": DynamicDelayText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicDelayText": "Dynamic Delay Text (Creepybits)",
}

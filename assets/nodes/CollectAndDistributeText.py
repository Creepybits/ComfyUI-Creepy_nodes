import time
import threading

class CollectAndDistributeText:
    def __init__(self):
        self.accumulated_text = ""
        self.timer = None
        self.lock = threading.Lock()  # Ensure thread safety

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seconds": ("FLOAT", {"default": 1.0, "min": 0.1, "step": 0.1}),
                "text": ("STRING", {"default": ""}),
                "trigger": ("BOOLEAN", {"default": False}),  # New trigger input
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "collect"
    CATEGORY = "Creepybits/Utilities"

    def collect(self, seconds, text, trigger):
        with self.lock:  # Thread-safe access to shared resources
            self.accumulated_text += text  # Append the new text

            if self.timer is not None:
                self.timer.cancel()  # Cancel any existing timer

            if trigger:  # If trigger is True, output immediately
                return self.output()
            else:
                self.timer = threading.Timer(seconds, self.timed_output)  # Start a new timer
                self.timer.start()
                return ("",)  # Return an empty string immediately

    def timed_output(self):
        with self.lock:
            output_text = self.accumulated_text
            self.accumulated_text = ""
            self.timer = None
        return (output_text,)

    def output(self):
        with self.lock:  # Thread-safe access to shared resources
            output_text = self.accumulated_text  # Copy the accumulated text
            self.accumulated_text = ""  # Reset the accumulated text
            self.timer = None  # Clear the timer

        return (output_text,)

NODE_CLASS_MAPPINGS = {
    "CollectAndDistributeText": CollectAndDistributeText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CollectAndDistributeText": "Collect and Distribute Text (Creepybits)",
}

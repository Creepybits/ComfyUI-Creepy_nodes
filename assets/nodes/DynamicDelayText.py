import time
import threading

class DynamicDelayText:
    def __init__(self):
        self.timer = None
        self.lock = threading.Lock()  
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
        with self.lock:  
            self.output_text = text  
            if self.timer is not None:
                self.timer.cancel()  
            self.timer = threading.Timer(seconds, self.output)  
            self.timer.start()
        return ("",)  

    def output(self):
        with self.lock: 
            text_to_output = self.output_text
            self.output_text = ""
            self.timer = None  
        return (text_to_output,)

NODE_CLASS_MAPPINGS = {
    "DynamicDelayText": DynamicDelayText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicDelayText": "Dynamic Delay Text (Creepybits)",
}

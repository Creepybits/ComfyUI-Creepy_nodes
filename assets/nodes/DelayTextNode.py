import time

class DelayTextNode:
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
        time.sleep(seconds)
        return (text,)


NODE_CLASS_MAPPINGS = {  
      "DelayTextNode": DelayTextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DelayTextNode": "Delay Text Node (Creepybits)",
}

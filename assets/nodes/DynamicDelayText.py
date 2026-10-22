import time


class DynamicDelayText:
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
        # This used to start a background timer and return "" immediately; the timer's result
        # had nowhere to go, so the node always output an empty string. Wait, then pass it on.
        time.sleep(seconds)
        return (text,)


NODE_CLASS_MAPPINGS = {
    "DynamicDelayText": DynamicDelayText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicDelayText": "Dynamic Delay Text (Creepybits)",
}

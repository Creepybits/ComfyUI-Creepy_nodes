import time

class DelayNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seconds": ("FLOAT", {"default": 1.0, "min": 0.1, "step": 0.1}),
                "image": ("IMAGE",),  
            },
        }

    RETURN_TYPES = ("IMAGE",)  
    RETURN_NAMES = ("image",)
    FUNCTION = "delay"
    CATEGORY = "Creepybits/Utilities"

    def delay(self, seconds, image):
        """
        Delays execution for the specified number of seconds.

        Args:
            seconds (float): The number of seconds to delay (minimum 0.1, step 0.1).
            image (torch.Tensor): The input image.

        Returns:
            torch.Tensor: The input image after the delay.
        """
        if seconds < 0.1:
            seconds = 0.1 

        time.sleep(seconds)
        return (image,)


NODE_CLASS_MAPPINGS = {  
      "DelayNode": DelayNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DelayNode": "Delay Node (Creepybits)",
}

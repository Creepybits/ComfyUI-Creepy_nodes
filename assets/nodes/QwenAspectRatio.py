class QwenAspectRatio:
    """
    A simple node to select from official Qwen aspect ratios and output width/height.
    """
    # Store the dictionary of aspect ratios as a class attribute
    ASPECT_RATIOS = {
        "1:1": (1328, 1328),
        "16:9": (1664, 928),
        "9:16": (928, 1664),
        "4:3": (1472, 1104),
        "3:4": (1104, 1472),
        "3:2": (1584, 1056),
        "2:3": (1056, 1584),
    }

    @classmethod
    def INPUT_TYPES(s):
        # The input is a dropdown menu populated by the keys of our dictionary
        return {
            "required": {
                "ratio": (list(s.ASPECT_RATIOS.keys()), ),
            }
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("width", "height",)
    FUNCTION = "get_dimensions"
    CATEGORY = "Creepybits/utils" # A new 'utils' category for helpful tools

    def get_dimensions(self, ratio):
        # Look up the selected ratio in our dictionary and return the width/height tuple
        width, height = self.ASPECT_RATIOS[ratio]
        return (width, height,)

# --- MAPPINGS ---
NODE_CLASS_MAPPINGS = {
    "QwenAspectRatioCreepy": QwenAspectRatio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenAspectRatioCreepy": "Qwen Aspect Ratio (Creepybits)",
}

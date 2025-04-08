class DynamicImageSwitch:

    def __init__(self):
        pass

    CATEGORY = "dynamic_switch"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("IMAGE", "show_help",)
    FUNCTION = "dynamic_switch"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        latent = None  # Initialize model to None

        if "image1" in kwargs and kwargs["image1"] is not None: #Check the kwarg model1 exists
            image = kwargs["image1"]  # Use model1 if it exists

        elif "image2" in kwargs and kwargs["image2"] is not None: #Check the kwarg model2 exists, to use the model
            image = kwargs["image2"]  # Use model2 if model1 is missing

        elif "image3" in kwargs and kwargs["image3"] is not None: #Check the kwarg model2 exists, to use the model
            image = kwargs["image3"]  # Use model2 if model1 is missing

        if image is not None:  # Return the model if a valid one was found
            return (image, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "DynamicImageSwitch": DynamicImageSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicImageSwitch": "Dynamic Image Switch (Creepybits)",
}

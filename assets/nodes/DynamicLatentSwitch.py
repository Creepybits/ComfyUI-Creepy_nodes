class DynamicLatentSwitch:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "latent1": ("LATENT",),
                "latent2": ("LATENT",),
                "latent3": ("LATENT",),
            }
        }

    RETURN_TYPES = ("LATENT", "STRING",)
    RETURN_NAMES = ("LATENT", "show_help",)
    FUNCTION = "dynamic_switch"
    CATEGORY = "Creepybits/Switches"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        latent = None  # Initialize model to None

        if "latent1" in kwargs and kwargs["latent1"] is not None: #Check the kwarg model1 exists
            latent = kwargs["latent1"]  # Use model1 if it exists

        elif "latent2" in kwargs and kwargs["latent2"] is not None: #Check the kwarg model2 exists, to use the model
            latent = kwargs["latent2"]  # Use model2 if model1 is missing

        elif "latent3" in kwargs and kwargs["latent3"] is not None: #Check the kwarg model2 exists, to use the model
            latent = kwargs["latent3"]  # Use model2 if model1 is missing

        if latent is not None:  # Return the model if a valid one was found
            return (latent, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "DynamicLatentSwitch": DynamicLatentSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicLatentSwitch": "Dynamic Latent Switch (Creepybits)",
}

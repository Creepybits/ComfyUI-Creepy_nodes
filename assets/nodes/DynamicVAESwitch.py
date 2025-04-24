class DynamicVAESwitch:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "vae1": ("VAE",),
                "vae2": ("VAE",),
                "vae3": ("VAE",),
            }
        }

    RETURN_TYPES = ("VAE", "STRING",)
    RETURN_NAMES = ("VAE", "show_help",)
    FUNCTION = "dynamic_switch"
    CATEGORY = "Creepybits/Switches"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        vae = None  # Initialize model to None

        if "vae1" in kwargs and kwargs["vae1"] is not None: #Check the kwarg model1 exists
            vae = kwargs["vae1"]  # Use model1 if it exists

        elif "vae2" in kwargs and kwargs["vae2"] is not None: #Check the kwarg model2 exists, to use the model
            vae = kwargs["vae2"]  # Use model2 if model1 is missing

        elif "vae3" in kwargs and kwargs["vae3"] is not None: #Check the kwarg model2 exists, to use the model
            vae = kwargs["vae3"]  # Use model2 if model1 is missing

        if vae is not None:  # Return the model if a valid one was found
            return (vae, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "DynamicVAESwitch": DynamicVAESwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicVAESwitch": "Dynamic VAE Switch (Creepybits)",
}

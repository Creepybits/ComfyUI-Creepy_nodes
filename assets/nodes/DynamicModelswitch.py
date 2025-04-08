class DynamicModelswitch:

    def __init__(self):
        pass

    CATEGORY = "dynamic_switch"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "model1": ("MODEL",),
                "model2": ("MODEL",),
                "model3": ("MODEL",),
            }
        }

    RETURN_TYPES = ("MODEL", "STRING",)
    RETURN_NAMES = ("MODEL", "show_help",)
    FUNCTION = "dynamic_switch"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        model = None  # Initialize model to None

        if "model1" in kwargs and kwargs["model1"] is not None: #Check the kwarg model1 exists
            model = kwargs["model1"]  # Use model1 if it exists

        elif "model2" in kwargs and kwargs["model2"] is not None: #Check the kwarg model2 exists, to use the model
            model = kwargs["model2"]  # Use model2 if model1 is missing

        elif "model3" in kwargs and kwargs["model3"] is not None: #Check the kwarg model2 exists, to use the model
            model = kwargs["model3"]  # Use model2 if model1 is missing

        if model is not None:  # Return the model if a valid one was found
            return (model, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "DynamicModelswitch": DynamicModelswitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicModelswitch": "Dynamic Model Switch (Creepybits)",
}

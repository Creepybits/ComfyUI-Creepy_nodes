class DynamicConditioning:

    def __init__(self):
        pass

    CATEGORY = "dynamic_switch"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "conditioning1": ("CONDITIONING",),
                "conditioning2": ("CONDITIONING",),
                "conditioning3": ("CONDITIONING",),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    RETURN_NAMES = ("CONDITIONING", "show_help",)
    FUNCTION = "dynamic_switch"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        cond = None  # Initialize model to None

        if "conditioning1" in kwargs and kwargs["conditioning1"] is not None: #Check the kwarg model1 exists
            conditioning = kwargs["conditioning1"]  # Use model1 if it exists

        elif "conditioning2" in kwargs and kwargs["conditioning2"] is not None: #Check the kwarg model2 exists, to use the model
            conditioning = kwargs["conditioning2"]  # Use model2 if model1 is missing

        elif "conditioning3" in kwargs and kwargs["conditioning3"] is not None: #Check the kwarg model2 exists, to use the model
            conditioning = kwargs["conditioning3"]  # Use model2 if model1 is missing

        if conditioning is not None:  # Return the model if a valid one was found
            return (conditioning, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "DynamicConditioning": DynamicConditioning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicConditioning": "Dynamic Conditioning (Creepybits)",
}

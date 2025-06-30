class DynamicModelswitch:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "model1": ("MODEL",),
                "model2": ("MODEL",),
                "model3": ("MODEL",),
                "model4": ("MODEL",),
            }
        }

    RETURN_TYPES = ("MODEL", "STRING",)
    RETURN_NAMES = ("MODEL", "show_help",)
    FUNCTION = "dynamic_switch"
    CATEGORY = "Creepybits/Switches"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        model = None  

        if "model1" in kwargs and kwargs["model1"] is not None: 
            model = kwargs["model1"] 

        elif "model2" in kwargs and kwargs["model2"] is not None: 
            model = kwargs["model2"] 

        elif "model3" in kwargs and kwargs["model3"] is not None: 
            model = kwargs["model3"]  

        elif "model4" in kwargs and kwargs["model4"] is not None: 
            model = kwargs["model4"]  

        if model is not None:  
            return (model, show_help,)
        else:
            return (None, show_help,)  


NODE_CLASS_MAPPINGS = {  
      "DynamicModelswitch": DynamicModelswitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicModelswitch": "Dynamic Model Switch (Creepybits)",
}

class DynamicConditioning:

    def __init__(self):
        pass

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
    CATEGORY = "Creepybits/Switches"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        cond = None  

        if "conditioning1" in kwargs and kwargs["conditioning1"] is not None: 
            conditioning = kwargs["conditioning1"]  

        elif "conditioning2" in kwargs and kwargs["conditioning2"] is not None: 
            conditioning = kwargs["conditioning2"]  

        elif "conditioning3" in kwargs and kwargs["conditioning3"] is not None: 
            conditioning = kwargs["conditioning3"]  

        if conditioning is not None: 
            return (conditioning, show_help,)
        else:
            return (None, show_help,)  


NODE_CLASS_MAPPINGS = {  
      "DynamicConditioning": DynamicConditioning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicConditioning": "Dynamic Conditioning (Creepybits)",
}

class DynamicImageSwitch:

    def __init__(self):
        pass

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
    CATEGORY = "Creepybits/Switches"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        latent = None  

        if "image1" in kwargs and kwargs["image1"] is not None: 
            image = kwargs["image1"]  

        elif "image2" in kwargs and kwargs["image2"] is not None: 
            image = kwargs["image2"]  

        elif "image3" in kwargs and kwargs["image3"] is not None: 
            image = kwargs["image3"]  

        if image is not None:  
            return (image, show_help,)
        else:
            return (None, show_help,) 


NODE_CLASS_MAPPINGS = { 
      "DynamicImageSwitch": DynamicImageSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicImageSwitch": "Dynamic Image Switch (Creepybits)",
}

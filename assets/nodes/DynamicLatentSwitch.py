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
        show_help = "Proverb of the day: I prefer not to think before speaking. I like being as surprised as everyone else by what comes out of my mouth."
        latent = None  

        if "latent1" in kwargs and kwargs["latent1"] is not None: 
            latent = kwargs["latent1"]  

        elif "latent2" in kwargs and kwargs["latent2"] is not None: 
            latent = kwargs["latent2"]  #

        elif "latent3" in kwargs and kwargs["latent3"] is not None: 
            latent = kwargs["latent3"]  #

        if latent is not None:  
            return (latent, show_help,)
        else:
            return (None, show_help,)  


NODE_CLASS_MAPPINGS = {  
      "DynamicLatentSwitch": DynamicLatentSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicLatentSwitch": "Dynamic Latent Switch (Creepybits)",
}

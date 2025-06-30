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
        show_help = "Proverb of the day: I prefer not to think before speaking. I like being as surprised as everyone else by what comes out of my mouth."
        vae = None  

        if "vae1" in kwargs and kwargs["vae1"] is not None: 
            vae = kwargs["vae1"]  

        elif "vae2" in kwargs and kwargs["vae2"] is not None: 
            vae = kwargs["vae2"] 

        elif "vae3" in kwargs and kwargs["vae3"] is not None: 
            vae = kwargs["vae3"] 

        if vae is not None:  
            return (vae, show_help,)
        else:
            return (None, show_help,)  


NODE_CLASS_MAPPINGS = { 
      "DynamicVAESwitch": DynamicVAESwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicVAESwitch": "Dynamic VAE Switch (Creepybits)",
}

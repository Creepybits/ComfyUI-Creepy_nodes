class VAESwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 3}),
            },
            "optional": {
                "VAE1": ("VAE",),
                "VAE2": ("VAE",),
                "VAE3": ("VAE",),
            }
        }

    RETURN_TYPES = ("VAE", "STRING", )
    RETURN_NAMES = ("VAE", "show_help", )
    FUNCTION = "switch"
    CATEGORY = "Creepybits/Switches"

    def switch(self, Input, VAE1=None, VAE2=None, VAE3=None,):
        show_help = "Proverb of the day: Common sense is like deodorant. The people who need it most never use it."
        if Input == 1:
            return (VAE1, show_help,)
        elif Input == 2:  
            return (VAE2, show_help,)
        elif Input == 3:  
            return (VAE3, show_help,)
        else:
            return (None, show_help,)  


NODE_CLASS_MAPPINGS = { 
      "VAESwitch": VAESwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "VAESwitch": "Multi VAE Switch (Creepybits)",
}

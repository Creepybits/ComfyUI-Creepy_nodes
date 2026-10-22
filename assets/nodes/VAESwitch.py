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
                "VAE1": ("VAE", {"lazy": True}),
                "VAE2": ("VAE", {"lazy": True}),
                "VAE3": ("VAE", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("VAE", "STRING", )
    RETURN_NAMES = ("VAE", "show_help", )
    FUNCTION = "switch"
    CATEGORY = "Creepybits/Switches"

    def check_lazy_status(self, Input, VAE1=None, VAE2=None, VAE3=None):
        # Only ask ComfyUI to evaluate the branch that is actually selected.
        if Input in (1, 2, 3):
            return [f"VAE{Input}"]
        return []

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

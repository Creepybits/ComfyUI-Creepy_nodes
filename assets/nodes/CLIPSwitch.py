class CLIPSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 3}),
            },
            "optional": {
                "clip1": ("CLIP", {"lazy": True}),
                "clip2": ("CLIP", {"lazy": True}),
                "clip3": ("CLIP", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("CLIP", "STRING", )
    RETURN_NAMES = ("CLIP", "show_help", )
    FUNCTION = "switch"
    CATEGORY = "Creepybits/Switches"

    def check_lazy_status(self, Input, clip1=None, clip2=None, clip3=None):
        # Only ask ComfyUI to evaluate the branch that is actually selected.
        if Input in (1, 2, 3):
            return [f"clip{Input}"]
        return []

    def switch(self, Input, clip1=None, clip2=None, clip3=None,):
        show_help = "Proverb of the day: Common sense is like deodorant. The people who need it most never use it."
        if Input == 1:
            return (clip1, show_help,)
        elif Input == 2:  
            return (clip2, show_help,)
        elif Input == 3:  
            return (clip3, show_help,)
        else:
            return (None, show_help,)  


NODE_CLASS_MAPPINGS = {  
      "CLIPSwitch": CLIPSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "CLIPSwitch": "Multi CLIP Switch (Creepybits)",
}

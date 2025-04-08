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
                "clip1": ("CLIP",),
                "clip2": ("CLIP",),
                "clip3": ("CLIP",),
            }
        }

    RETURN_TYPES = ("CLIP", "STRING", )
    RETURN_NAMES = ("CLIP", "show_help", )
    FUNCTION = "switch"

    def switch(self, Input, clip1=None, clip2=None, clip3=None,):
        show_help = "Proverb of the day: Common sense is like deodorant. The people who need it most never use it."
        if Input == 1:
            return (clip1, show_help,)
        elif Input == 2:  # Corrected indentation
            return (clip2, show_help,)
        elif Input == 3:  # Corrected indentation
            return (clip3, show_help,)
        else:
            return (None, show_help,)  # Handle invalid input (return None model)


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "CLIPSwitch": CLIPSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "CLIPSwitch": "Multi CLIP Switch (Creepybits)",
}

class Textswitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 3}),
            },
            "optional": {
                "text1": ("STRING",),
                "text2": ("STRING",),
                "text3": ("STRING",),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help",)
    FUNCTION = "switch"
    CATEGORY = "Creepybits/Switches"

    def switch(self, Input, text1=None, text2=None, text3=None,):
        show_help = "Proverb of the day: Something about today makes me want to have a hangover tomorrow."
        if Input == 1:
            return (text1, show_help,)
        elif Input == 2:  # Corrected indentation
            return (text2, show_help,)
        elif Input == 3:  # Corrected indentation
            return (text3, show_help,)
        else:
            return (None, show_help,)  # Handle invalid input (return None model)


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "Textswitch": Textswitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "Textswitch": "Text Switch (Creepybits)",
}

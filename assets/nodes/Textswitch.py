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
                "text1": ("STRING", {"lazy": True}),
                "text2": ("STRING", {"lazy": True}),
                "text3": ("STRING", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("STRING", "show_help",)
    FUNCTION = "switch"
    CATEGORY = "Creepybits/Switches"

    def check_lazy_status(self, Input, text1=None, text2=None, text3=None):
        # Only ask ComfyUI to evaluate the branch that is actually selected.
        if Input in (1, 2, 3):
            return [f"text{Input}"]
        return []

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

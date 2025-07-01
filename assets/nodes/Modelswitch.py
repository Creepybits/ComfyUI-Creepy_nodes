class Modelswitch:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Input": ("INT", {"default": 1, "min": 1, "max": 3}),
            },
            "optional": {
                "model1": ("MODEL",),
                "model2": ("MODEL",),
                "model3": ("MODEL",),
            }
        }

    RETURN_TYPES = ("MODEL", "STRING", )
    RETURN_NAMES = ("MODEL", "show_help", )
    FUNCTION = "switch"
    CATEGORY = "Creepybits/Switches"

    def switch(self, Input, model1=None, model2=None, model3=None):
        show_help = "Proverb of the day: Everyone has the right to do stupid things, but you’re abusing that privilege."
        if Input == 1:
            return (model1, show_help,)
        elif Input == 2:  
            return (model2, show_help,)
        elif Input == 3:  
            return (model3, show_help,)
        else:
            return (None, show_help,)  

NODE_CLASS_MAPPINGS = {  
      "Modelswitch": Modelswitch, 
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "Modelswitch": "Multi Model Switch (Creepybits)",
}

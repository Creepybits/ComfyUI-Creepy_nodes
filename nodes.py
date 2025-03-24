from inspect import cleandoc
class Modelswitch:

    def __init__(self):
        pass
    CATEGORY = "switch"
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

    def switch(self, Input, model1=None, model2=None, model3=None):
        show_help = "Proverb of the day: Everyone has the right to do stupid things, but you’re abusing that privilege."
        if Input == 1:
            return (model1, show_help,)
        elif Input == 2:  # Corrected indentation
            return (model2, show_help,)
        elif Input == 3:  # Corrected indentation
            return (model3, show_help,)
        else:
            return (None, show_help,)  # Handle invalid input (return None model)

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

    def switch(self, Input, VAE1=None, VAE2=None, VAE3=None,):
        show_help = "Proverb of the day: Common sense is like deodorant. The people who need it most never use it."
        if Input == 1:
            return (VAE1, show_help,)
        elif Input == 2:  # Corrected indentation
            return (VAE2, show_help,)
        elif Input == 3:  # Corrected indentation
            return (VAE3, show_help,)
        else:
            return (None, show_help,)  # Handle invalid input (return None model)

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

class DynamicModelswitch:

    def __init__(self):
        pass

    CATEGORY = "dynamic_switch"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "model1": ("MODEL",),
                "model2": ("MODEL",),
                "model3": ("MODEL",),
            }
        }

    RETURN_TYPES = ("MODEL", "STRING",)
    RETURN_NAMES = ("MODEL", "show_help",)
    FUNCTION = "dynamic_switch"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        model = None  # Initialize model to None

        if "model1" in kwargs and kwargs["model1"] is not None: #Check the kwarg model1 exists
            model = kwargs["model1"]  # Use model1 if it exists

        elif "model2" in kwargs and kwargs["model2"] is not None: #Check the kwarg model2 exists, to use the model
            model = kwargs["model2"]  # Use model2 if model1 is missing

        elif "model3" in kwargs and kwargs["model3"] is not None: #Check the kwarg model2 exists, to use the model
            model = kwargs["model3"]  # Use model2 if model1 is missing

        if model is not None:  # Return the model if a valid one was found
            return (model, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided

class DynamicClipswitch:

    def __init__(self):
        pass

    CATEGORY = "dynamic_clip_switch"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},  # or None is also valid
            "optional": {
                "clip1": ("CLIP",),
                "clip2": ("CLIP",),
                "clip3": ("CLIP",),
            }
        }

    RETURN_TYPES = ("CLIP", "STRING",)
    RETURN_NAMES = ("CLIP", "show_help",)
    FUNCTION = "dynamic_clip_switch"

    def dynamic_clip_switch(self, clip1: "CLIP" = None, clip2: "CLIP" = None, clip3: "CLIP" = None):  #<---Fixed parameters
        show_help = "Proverb of the day: I prefer not to think before speaking. I like being as surprised as everyone else by what comes out of my mouth."
        clip = None  # Initialize clip to None

        if clip1 is not None: #Check the kwarg clip1 exists
            clip = clip1  # Use clip1 if it exists

        elif clip2 is not None: #Check the kwarg clip2 exists, to use the clip
            clip = clip2  # Use clip2 if clip1 is missing

        elif clip3 is not None: #Check the kwarg clip3 exists, to use the clip
            clip = clip3  # Use clip3 if clip1 is missing

        if clip is not None:  # Return the clip if a valid one was found
            return (clip, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid clips were provided

class Textswitch:
    def __init__(self):
        pass

        CATEGORY = "switch"

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
    "Modelswitch": Modelswitch, #Corrected Node name
    "VAESwitch": VAESwitch,
    "CLIPSwitch": CLIPSwitch,
    "DynamicModelswitch": DynamicModelswitch,
    "DynamicClipswitch": DynamicClipswitch,
    "Textswitch": Textswitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Modelswitch": "Multi Model Switch (Creepybits)",
    "VAESwitch": "Multi VAE Switch (Creepybits)",
    "CLIPSwitch": "Multi CLIP Switch (Creepybits)",
    "DynamicModelswitch": "Dynamic Model Switch (Creepybits)",
    "DynamicClipswitch": "Dynamic Clip Switch (Creepybits)",# <---Outdent these lines
    "Textswitch": "Text Switch (Creepybits)",
}

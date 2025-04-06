from inspect import cleandoc
import folder_paths  # Import folder_paths
import comfy.sd
import comfy.utils
import os
import time


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

class DynamicConditioning:

    def __init__(self):
        pass

    CATEGORY = "dynamic_switch"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "conditioning1": ("CONDITIONING",),
                "conditioning2": ("CONDITIONING",),
                "conditioning3": ("CONDITIONING",),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    RETURN_NAMES = ("CONDITIONING", "show_help",)
    FUNCTION = "dynamic_switch"

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        cond = None  # Initialize model to None

        if "conditioning1" in kwargs and kwargs["conditioning1"] is not None: #Check the kwarg model1 exists
            conditioning = kwargs["conditioning1"]  # Use model1 if it exists

        elif "conditioning2" in kwargs and kwargs["conditioning2"] is not None: #Check the kwarg model2 exists, to use the model
            conditioning = kwargs["conditioning2"]  # Use model2 if model1 is missing

        elif "conditioning3" in kwargs and kwargs["conditioning3"] is not None: #Check the kwarg model2 exists, to use the model
            conditioning = kwargs["conditioning3"]  # Use model2 if model1 is missing

        if conditioning is not None:  # Return the model if a valid one was found
            return (conditioning, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided


class DynamicLatentSwitch:

    def __init__(self):
        pass

    CATEGORY = "dynamic_switch"

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

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        latent = None  # Initialize model to None

        if "latent1" in kwargs and kwargs["latent1"] is not None: #Check the kwarg model1 exists
            latent = kwargs["latent1"]  # Use model1 if it exists

        elif "latent2" in kwargs and kwargs["latent2"] is not None: #Check the kwarg model2 exists, to use the model
            latent = kwargs["latent2"]  # Use model2 if model1 is missing

        elif "latent3" in kwargs and kwargs["latent3"] is not None: #Check the kwarg model2 exists, to use the model
            latent = kwargs["latent3"]  # Use model2 if model1 is missing

        if latent is not None:  # Return the model if a valid one was found
            return (latent, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided


class DynamicVAESwitch:

    def __init__(self):
        pass

    CATEGORY = "dynamic_switch"

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

    def dynamic_switch(self, **kwargs):
        show_help = "Proverb of the day: Freedom means the right to yell, “THEATRE!” in a crowded fire."
        vae = None  # Initialize model to None

        if "vae1" in kwargs and kwargs["vae1"] is not None: #Check the kwarg model1 exists
            vae = kwargs["vae1"]  # Use model1 if it exists

        elif "vae2" in kwargs and kwargs["vae2"] is not None: #Check the kwarg model2 exists, to use the model
            vae = kwargs["vae2"]  # Use model2 if model1 is missing

        elif "vae3" in kwargs and kwargs["vae3"] is not None: #Check the kwarg model2 exists, to use the model
            vae = kwargs["vae3"]  # Use model2 if model1 is missing

        if vae is not None:  # Return the model if a valid one was found
            return (vae, show_help,)
        else:
            return (None, show_help,)  # Return None if no valid models were provided

class SystemPrompt:

    def __init__(self):
        # Get the directory of the current script (systemprompt.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the text file
        filepath = os.path.join(script_dir, "system_prompt.txt")  # or "path/to/your/textfile.txt" if it's in a subdirectory

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.fixed_text = f.read()
        except FileNotFoundError:
            print(f"Error: system_prompt.txt not found at {filepath}")
            self.fixed_text = "ERROR: Prompt file not found."  # Provide a fallback
        except Exception as e:
            print(f"Error reading system_prompt.txt: {e}")
            self.fixed_text = "ERROR: Could not read prompt file."  # Provide a fallback

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_2": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    FUNCTION = "concat_texts"

    CATEGORY = "Creepybits/Prompt"

    def concat_texts(self, text_2):
        combined_text = self.fixed_text + text_2
        return (combined_text,)


class DelayNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seconds": ("FLOAT", {"default": 1.0, "min": 0.1, "step": 0.1}),
                "image": ("IMAGE",),  # Specific input type for images
            },
        }

    RETURN_TYPES = ("IMAGE",)  # Specific return type for images
    RETURN_NAMES = ("image",)
    FUNCTION = "delay"
    CATEGORY = "Utilities"

    def delay(self, seconds, image):
        """
        Delays execution for the specified number of seconds.

        Args:
            seconds (float): The number of seconds to delay (minimum 0.1, step 0.1).
            image (torch.Tensor): The input image.

        Returns:
            torch.Tensor: The input image after the delay.
        """
        if seconds < 0.1:
            seconds = 0.1 #Enforce minimum value.

        time.sleep(seconds)
        return (image,)


class DelayTextNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seconds": ("FLOAT", {"default": 1.0, "min": 0.1, "step": 0.1}),
                "text": ("STRING",),  # Text input
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "delay"
    CATEGORY = "Utilities"

    def delay(self, seconds, text):
        time.sleep(seconds)
        return (text,)



NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
    "Modelswitch": Modelswitch, #Corrected Node name
    "VAESwitch": VAESwitch,
    "CLIPSwitch": CLIPSwitch,
    "DynamicModelswitch": DynamicModelswitch,
    "DynamicClipswitch": DynamicClipswitch,
    "Textswitch": Textswitch,
    "DynamicConditioning": DynamicConditioning,
    "DynamicLatentSwitch": DynamicLatentSwitch,
    "DynamicVAESwitch": DynamicVAESwitch,
    "SystemPromp": SystemPrompt,
    "DelayNode": DelayNode,
    "DelayTextNode": DelayTextNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Modelswitch": "Multi Model Switch (Creepybits)",
    "VAESwitch": "Multi VAE Switch (Creepybits)",
    "CLIPSwitch": "Multi CLIP Switch (Creepybits)",
    "DynamicModelswitch": "Dynamic Model Switch (Creepybits)",
    "DynamicClipswitch": "Dynamic Clip Switch (Creepybits)",# <---Outdent these lines
    "Textswitch": "Text Switch (Creepybits)",
    "DynamicConditioning": "Dynamic Conditioning (Creepybits)",
    "DynamicLatentSwitch": "Dynamic Latent Switch (Creepybits)",
    "DynamicVAESwitch": "Dynamic VAE Switch (Creepybits)",
    "SystemPromp": "System Prompt (Creepybits)",
    "DelayNode": "Delay Image Node (Creepybits)",
    "DelayTextNode": "Delay Text Node (Creepybits)",
}

class DynamicClipswitch:

    def __init__(self):
        pass

    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},  
            "optional": {
                "clip1": ("CLIP",),
                "clip2": ("CLIP",),
                "clip3": ("CLIP",),
            }
        }

    RETURN_TYPES = ("CLIP", "STRING",)
    RETURN_NAMES = ("CLIP", "show_help",)
    FUNCTION = "dynamic_clip_switch"
    CATEGORY = "Creepybits/Switches"

    def dynamic_clip_switch(self, clip1: "CLIP" = None, clip2: "CLIP" = None, clip3: "CLIP" = None):  
        show_help = "Proverb of the day: I prefer not to think before speaking. I like being as surprised as everyone else by what comes out of my mouth."
        clip = None  

        if clip1 is not None: 
            clip = clip1  

        elif clip2 is not None: 
            clip = clip2 

        elif clip3 is not None: 
            clip = clip3  

        if clip is not None:  
            return (clip, show_help,)
        else:
            return (None, show_help,)  


NODE_CLASS_MAPPINGS = { 
      "DynamicClipswitch": DynamicClipswitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicClipswitch": "Dynamic Clip Switch (Creepybits)",
}

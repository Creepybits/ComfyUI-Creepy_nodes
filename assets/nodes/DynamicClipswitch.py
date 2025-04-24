class DynamicClipswitch:

    def __init__(self):
        pass

    
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
    CATEGORY = "Creepybits/Switches"

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


NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
      "DynamicClipswitch": DynamicClipswitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "DynamicClipswitch": "Dynamic Clip Switch (Creepybits)",
}

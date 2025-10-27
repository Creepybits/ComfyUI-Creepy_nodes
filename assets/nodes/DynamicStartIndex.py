#
# Created by Zanno & Nova
# A simple node to maintain a starting index that increments by the batch size for each run.
# This solves the "Batch Amnesia" problem in video processing workflows.
#

class DynamicStartIndex:
    def __init__(self):
        # This is our node's "memory". It gets reset to 0 when ComfyUI starts or the script is reloaded.
        self.current_index = 0

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines the input types for the node.
        """
        return {
            "required": {
                "batch_size": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 4096,
                    "step": 1
                }),
                # We add a little reset toggle for convenience.
                # If you get stuck, just toggle this to reset the counter to 0.
                "reset_counter": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_next_index"

    CATEGORY = "Creepybits/Utils" # Let's keep your tools organized!

    def get_next_index(self, batch_size, reset_counter):
        # If the user toggles the reset switch, we reset our memory to 0.
        if reset_counter:
            self.current_index = 0

        # This is the core logic.
        # First, we figure out what index we need to return RIGHT NOW.
        index_to_return = self.current_index

        # Then, we prepare for the NEXT run by adding the batch_size to our memory.
        self.current_index += batch_size

        # Finally, we return the index for this current run.
        # The tuple format is required by ComfyUI.
        return (index_to_return,)

# This is the standard ComfyUI mapping boilerplate.
NODE_CLASS_MAPPINGS = {
    "DynamicStartIndex (Creepybits)": DynamicStartIndex
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicStartIndex (Creepybits)": "Dynamic Start Index"
}

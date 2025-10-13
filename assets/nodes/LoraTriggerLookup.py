import json
import os
import folder_paths

# --- Get a list of all LoRA files ---
# This code runs once when ComfyUI starts up.
lora_paths = folder_paths.get_filename_list("loras")
lora_files = [os.path.basename(x) for x in lora_paths if x is not None]
# Add a "None" option to the beginning of the list for when no LoRA is selected
lora_files.insert(0, "None")


class LoraTriggerLookup:
    """
    A standalone node to select a LoRA and look up its trigger words from a central JSON file.
    """
    # Define the path to our database file
    JSON_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Lora_db', 'lora_triggers.json')

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # The dropdown menu will be populated with all of your LoRA files
                "lora_name": (lora_files,),
                "num_triggers": ("INT", {"default": -1, "min": -1, "max": 20, "step": 1}),
                "delimiter": ("STRING", {"default": ", "}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("trigger_words",)
    FUNCTION = "get_triggers"
    CATEGORY = "Creepybits/text"

    def get_triggers(self, lora_name, num_triggers, delimiter):
        output_triggers = ""

        # If the user selects "None", do nothing.
        if lora_name == "None":
            return ("",)

        try:
            with open(self.JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                lora_database = json.load(f)

            if lora_name in lora_database:
                all_triggers = lora_database[lora_name]

                if all_triggers:
                    triggers_to_use = []
                    if num_triggers == -1:
                        triggers_to_use = all_triggers
                    else:
                        triggers_to_use = all_triggers[:num_triggers]

                    output_triggers = delimiter.join(triggers_to_use)
                    print(f"LoraTriggerLookup: Found '{lora_name}'. Outputting triggers: {output_triggers}")
                else:
                    print(f"LoraTriggerLookup: Found '{lora_name}' but it has no listed triggers.")
            else:
                print(f"LoraTriggerLookup: LoRA '{lora_name}' not found in the database. Consider adding it.")

        except FileNotFoundError:
            print(f"LoraTriggerLookup ERROR: The database file was not found at {self.JSON_FILE_PATH}. Please create it.")
        except Exception as e:
            print(f"LoraTriggerLookup ERROR: An unexpected error occurred: {e}")

        return (output_triggers,)


# --- MAPPINGS ---
NODE_CLASS_MAPPINGS = {
    "LoraTriggerLookup": LoraTriggerLookup,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraTriggerLookup": "LoRA Trigger Lookup (Creepybits)",
}

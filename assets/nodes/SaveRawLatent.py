import torch
import os
import folder_paths
import datetime


class SaveRawLatent:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT",),
                "folder_path": ("STRING", {"default": "latents"}),
                "filename": ("STRING", {"default": "MyLatentBlend"})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "Creepybits/latent"

    def save(self, samples, folder_path, filename):
        try:
            # Extract the raw tensor, this is the most important step
            tensor_to_save = samples["samples"]

            # Manually construct the full output path
            full_folder_path = os.path.join(self.output_dir, folder_path)

            # Create the directory if it doesn't exist
            os.makedirs(full_folder_path, exist_ok=True)

            # Create a unique filename with a timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            full_path = os.path.join(full_folder_path, f"{filename}_{timestamp}.latent")

            # Save the raw tensor. This is the critical command.
            torch.save(tensor_to_save, full_path)

            print(f"Creepy Latent Saver V2: Successfully saved RAW latent to: {full_path}")

        except Exception as e:
            print(f"Creepy Latent Saver V2 Error: Failed to save latent. Reason: {e}")

        return {}


# --- MAPPINGS ---
NODE_CLASS_MAPPINGS = {
    "SaveRawLatent": SaveRawLatent,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveRawLatent": "Save Raw Latent (Creepybits)",
}

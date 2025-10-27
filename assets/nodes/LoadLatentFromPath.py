import torch
import os
import folder_paths

class LoadLatentFromPath:
    """
    A custom node to load a latent file from any specified path relative to the ComfyUI base directory.
    This allows for better organization by loading latents from the 'output' folder or any subfolders.
    """
    @classmethod
    def INPUT_TYPES(s):
        # This defines the inputs that the user will see in the ComfyUI interface.
        return {
            "required": {
                "latent_path": ("STRING", {
                    "multiline": False,
                    "default": "output/my_latents/latent_sample.latent"
                }),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "load_latent"
    CATEGORY = "Creepybits/loaders" # This will put our node in the latent > loaders submenu

    def load_latent(self, latent_path):
        # Construct the full path. This assumes the path is relative to the main ComfyUI directory.
        full_path = os.path.join(folder_paths.get_input_directory(), '..', latent_path)

        try:
            # Load the tensor from the file
            latent_tensor = torch.load(full_path, map_location=torch.device('cpu'))

            # ComfyUI expects latents in a dictionary format
            latent = {"samples": latent_tensor}
            print(f"Successfully loaded latent from: {full_path}")

        except FileNotFoundError:
            print(f"Error: Latent file not found at {full_path}")
            # If the file isn't found, return a default empty latent to prevent crashing the workflow.
            # This creates a standard 1024x1024 (128x128 latent) empty tensor.
            latent = {"samples": torch.zeros([1, 4, 128, 128])}

        except Exception as e:
            print(f"An unexpected error occurred while loading latent: {e}")
            latent = {"samples": torch.zeros([1, 4, 128, 128])}

        return (latent,)

# This is the standard boilerplate to tell ComfyUI about our new node.
NODE_CLASS_MAPPINGS = {
    "LoadLatentFromPath": LoadLatentFromPath
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadLatentFromPath": "Load Latent From Path (Creepybits)"
}

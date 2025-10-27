import torch
import os
import folder_paths
import datetime
import numpy as np # <-- We've called in the cavalry

class LoadLatentFromPath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latent_path": ("STRING", {"multiline": False, "default": "output/latents/MyLatent_00001.latent"}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "load_latent"
    CATEGORY = "Creepybits/latent"

    def load_latent(self, latent_path):
        full_path = os.path.join(folder_paths.get_input_directory(), '..', latent_path)
        try:
            # We must now load the raw bytes and reshape them back into a tensor
            with open(full_path, 'rb') as f:
                raw_bytes = f.read()

            # The shape for a float32 128x128 latent is (1, 4, 128, 128)
            # The shape for a float16 128x128 latent is also (1, 4, 128, 128) but uses half the bytes
            # We will assume float32 for now as it is the most common for non-SDXL VAEs
            # Note: This loader will now ONLY work with latents saved by our new saver.

            # Let's check the file size to guess the dtype
            file_size = os.path.getsize(full_path)
            expected_float32_size = 1 * 4 * 128 * 128 * 4 # (batch, channels, h, w, bytes_per_float32)

            if file_size == expected_float32_size:
                dtype = np.float32
            else:
                # Assuming float16 for SDXL latents, which are ~half the size
                dtype = np.float16

            numpy_array = np.frombuffer(raw_bytes, dtype=dtype).reshape(1, 4, 128, 128)
            latent_tensor = torch.from_numpy(numpy_array)
            latent = {"samples": latent_tensor}
            print(f"Creepy Raw Loader: Successfully loaded RAW latent from: {full_path}")
        except Exception as e:
            print(f"Creepy Raw Loader Error: Could not load raw latent from {full_path}. Reason: {e}")
            latent = {"samples": torch.zeros([1, 4, 128, 128])}
        return (latent,)

class SaveRawLatent:
    @classmethod
    def INPUT_TYPES(s):
        return { "required": {
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
            tensor_to_save = samples["samples"]

            # Convert to a CPU numpy array. This is a crucial step.
            numpy_array = tensor_to_save.cpu().numpy()

            full_folder_path = os.path.join(folder_paths.get_output_directory(), folder_path)
            os.makedirs(full_folder_path, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            full_path = os.path.join(full_folder_path, f"{filename}_{timestamp}.latent")

            # Open the file in binary write mode and write the raw bytes
            with open(full_path, 'wb') as f:
                f.write(numpy_array.tobytes())

            print(f"Creepy Raw Saver V3: Successfully saved RAW BYTES to: {full_path}")
        except Exception as e:
            print(f"Creepy Raw Saver V3 Error: Failed to save latent. Reason: {e}")
        return {}

# --- MAPPINGS ---
NODE_CLASS_MAPPINGS = {
    "LoadLatentFromPathCreepy": LoadLatentFromPath,
    "SaveRawLatentCreepy": SaveRawLatent,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadLatentFromPathCreepy": "Load Raw Latent (Creepybits)",
    "SaveRawLatentCreepy": "Save Raw Latent (Creepybits)",
}

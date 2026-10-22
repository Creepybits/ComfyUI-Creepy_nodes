import torch
import os
import folder_paths
import datetime
import numpy as np
import safetensors.torch

# Shape that the old raw-bytes format implicitly assumed (it stored no shape or dtype).
LEGACY_RAW_SHAPE = (1, 4, 128, 128)


def _load_legacy_raw(full_path):
    """Reads a latent written by the old raw-bytes saver (only 1x4x128x128 is possible)."""
    file_size = os.path.getsize(full_path)
    elements = int(np.prod(LEGACY_RAW_SHAPE))
    if file_size == elements * 4:
        dtype = np.float32
    elif file_size == elements * 2:
        dtype = np.float16
    else:
        raise ValueError(f"not a safetensors latent, and its size ({file_size} bytes) doesn't match the legacy 1x4x128x128 raw format")
    with open(full_path, 'rb') as f:
        numpy_array = np.frombuffer(f.read(), dtype=dtype).reshape(LEGACY_RAW_SHAPE)
    return torch.from_numpy(numpy_array.copy())


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

    @classmethod
    def IS_CHANGED(cls, latent_path):
        full_path = os.path.join(folder_paths.base_path, latent_path)
        return os.path.getmtime(full_path) if os.path.exists(full_path) else ""

    def load_latent(self, latent_path):
        # The path is relative to the ComfyUI folder (absolute paths work too).
        full_path = os.path.join(folder_paths.base_path, latent_path)
        try:
            try:
                # Current format: safetensors, same layout as ComfyUI's built-in Save/Load Latent,
                # so any latent shape (SDXL, Flux, video, ...) round-trips correctly.
                latent_tensor = safetensors.torch.load_file(full_path, device="cpu")["latent_tensor"].float()
            except (safetensors.SafetensorError, KeyError):
                latent_tensor = _load_legacy_raw(full_path)
            latent = {"samples": latent_tensor}
            print(f"Creepy Raw Loader: Successfully loaded latent from: {full_path}")
        except Exception as e:
            print(f"Creepy Raw Loader Error: Could not load latent from {full_path}. Reason: {e}")
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
            tensor_to_save = samples["samples"].contiguous().cpu()

            full_folder_path = os.path.join(folder_paths.get_output_directory(), folder_path)
            os.makedirs(full_folder_path, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            full_path = os.path.join(full_folder_path, f"{filename}_{timestamp}.latent")

            # "latent_format_version_0" marks the file as unscaled for ComfyUI's built-in Load Latent.
            output = {"latent_tensor": tensor_to_save, "latent_format_version_0": torch.tensor([])}
            safetensors.torch.save_file(output, full_path)

            print(f"Creepy Raw Saver: Successfully saved latent {tuple(tensor_to_save.shape)} to: {full_path}")
        except Exception as e:
            print(f"Creepy Raw Saver Error: Failed to save latent. Reason: {e}")
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

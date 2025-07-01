import os
import torch
from PIL import ImageOps
try:
    import pillow_jxl      # noqa: F401
    jxl = True
except ImportError:
    jxl = False
import comfy
import folder_paths
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import logging
import time


class LoadBatchImagesDir:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "image_load_cap": ("INT", {"default": 0, "min": 0, "step": 1}),
                "start_index": ("INT", {"default": 0, "min": -1, "max": 0xffffffffffffffff, "step": 1}),
                "load_always": ("BOOLEAN", {"default": False, "label_on": "enabled", "label_off": "disabled"}),
                "force_rescan": ("BOOLEAN", {"default": False, "label_on": "Rescan/Revalidate", "label_off": "Use Cache"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT")
    FUNCTION = "load_images"

    CATEGORY = "Creepybits/image"

    def __init__(self):
        self._cached_dir = None
        self._cached_image_files = None
        self._cached_dir_mtime = None


    @classmethod
    def IS_CHANGED(cls, **kwargs):
        if 'load_always' in kwargs and kwargs['load_always']:
            return float("NaN")
        else:
            relevant_kwargs = {k: v for k, v in kwargs.items() if k in ['directory', 'image_load_cap', 'start_index', 'force_rescan']}
            return hash(frozenset(relevant_kwargs.items()))


    def load_images(self, directory: str, image_load_cap: int = 0, start_index: int = 0, load_always=False, force_rescan=False):
        if not os.path.isdir(directory):
            print(f"LoadBatchImagesDir ERROR: Directory '{directory}' not found.")
            self._cached_dir = None
            self._cached_image_files = None
            self._cached_dir_mtime = None
            raise FileNotFoundError(f"Directory '{directory} cannot be found.'")

        current_dir_mtime = os.path.getmtime(directory)

        needs_full_scan = False
        if force_rescan or self._cached_dir is None or self._cached_dir != directory or self._cached_dir_mtime is None or self._cached_dir_mtime < current_dir_mtime:
            needs_full_scan = True

        if needs_full_scan:
            dir_files = os.listdir(directory)

            if not dir_files:
                print(f"LoadBatchImagesDir ERROR: No files found in directory '{directory}'.")
                self._cached_dir = directory
                self._cached_image_files = []
                self._cached_dir_mtime = current_dir_mtime
                raise FileNotFoundError(f"No files in directory '{directory}'.")

            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.jxl', '.gif', '.bmp', '.tiff', '.ico']
            image_files_potential = []

            for filename in dir_files:
                if any(filename.lower().endswith(ext) for ext in valid_extensions):
                    full_path = os.path.join(directory, filename)
                    try:
                        with Image.open(full_path) as img:
                            img.verify()
                        image_files_potential.append(filename)
                    except (IOError, SyntaxError) as e:
                        print(f"LoadBatchImagesDir WARNING: Skipping file due to PIL error during validation: {filename} - {e}")
                    except Exception as e:
                        print(f"LoadBatchImagesDir WARNING: Skipping file: {filename} - {type(e).__name__} - {e}")

            if not image_files_potential:
                print(f"LoadBatchImagesDir ERROR: No valid images found in directory '{directory}' after filtering.")
                self._cached_dir = directory
                self._cached_image_files = []
                self._cached_dir_mtime = current_dir_mtime
                raise FileNotFoundError(f"No valid images found in directory '{directory}'.")

            image_files_potential = sorted(image_files_potential)

            self._cached_dir = directory
            self._cached_image_files = image_files_potential
            self._cached_dir_mtime = current_dir_mtime

        else:
            image_files_potential = self._cached_image_files

            if not image_files_potential:
                 print(f"LoadBatchImagesDir ERROR: Cached image list for '{directory}' is empty.")
                 raise FileNotFoundError(f"No valid images found in directory '{directory}'.")


        actual_start_index = start_index
        if start_index < 0 or start_index >= len(image_files_potential):
             print(f"LoadBatchImagesDir WARNING: start_index {start_index} is out of range for {len(image_files_potential)} valid images. Using 0.")
             actual_start_index = 0

        image_files_to_load = image_files_potential[actual_start_index:]

        if image_load_cap > 0:
             image_files_to_load = image_files_to_load[:image_load_cap]

        if not image_files_to_load:
             print(f"LoadBatchImagesDir ERROR: No images selected to load after applying start_index ({actual_start_index}) and load_cap ({image_load_cap}) to {len(image_files_potential)} valid images.")
             raise FileNotFoundError(f"No images selected to load from '{directory}' with specified index and cap.")


        image_paths_to_load = [os.path.join(directory, x) for x in image_files_to_load]

        images = []
        masks = []
        loaded_image_count = 0

        for image_path in image_paths_to_load:
            try:
                with Image.open(image_path) as i:
                    i = ImageOps.exif_transpose(i)
                    image = i.convert("RGB")
                    image = np.array(image).astype(np.float32) / 255.0
                    image = torch.from_numpy(image)[None,]

                    if 'A' in i.getbands():
                        mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                        mask = 1. - torch.from_numpy(mask)
                        mask = mask.unsqueeze(0)
                    else:
                        mask = torch.ones((image.shape[1], image.shape[2]), dtype=torch.float32, device="cpu").unsqueeze(0)

                    images.append(image)
                    masks.append(mask)
                    loaded_image_count += 1

            except Exception as e:
                print(f"LoadBatchImagesDir WARNING: Error processing image {os.path.basename(image_path)} during loading: {e}. Skipping this image.")
                continue

        if not images:
            print(f"LoadBatchImagesDir ERROR: No images could be loaded from the selected subset of '{directory}'.")
            raise FileNotFoundError(f"No images could be loaded from the selected subset of '{directory}'.")


        final_image_batch = images[0]
        final_mask_batch = masks[0]

        for idx in range(1, len(images)):
            image2 = images[idx]
            mask2 = masks[idx]

            target_height = image_batch.shape[1]
            target_width = image_batch.shape[2]
            target_size = (target_height, target_width)

            if image2.shape[1:3] != target_size:
                image2_upscaled = comfy.utils.common_upscale(
                    image2.movedim(-1, 1),
                    target_width,
                    target_height,
                    "bilinear",
                    "center"
                ).movedim(1, -1)
                if image2_upscaled.shape[1:3] != target_size:
                     print(f"LoadBatchImagesDir ERROR: Image upscaling failed to reach target size {target_size} during batching. Got {image2_upscaled.shape[1:3]}")
                     raise RuntimeError(f"Image upscaling failed for a successfully loaded image during batching.")
                final_image_batch = torch.cat((final_image_batch, image2_upscaled), dim=0)
            else:
                final_image_batch = torch.cat((final_image_batch, image2), dim=0)


            if mask2.shape[1:3] != target_size:
                mask2_interp_input = mask2.unsqueeze(1)

                mask2_upscaled_interp = torch.nn.functional.interpolate(
                    mask2_interp_input,
                    size=target_size,
                    mode='bilinear',
                    align_corners=False
                )

                mask2_upscaled = mask2_upscaled_interp.squeeze(1)

                if mask2_upscaled.shape[1:3] != target_size:
                     print(f"LoadBatchImagesDir ERROR: Mask upscaling failed to reach target size {target_size} during batching. Got {mask2_upscaled.shape[1:3]}")
                     raise RuntimeError(f"Mask upscaling failed for a successfully loaded mask during batching.")

                final_mask_batch = torch.cat((final_mask_batch, mask2_upscaled), dim=0)
            else:
                 final_mask_batch = torch.cat((final_mask_batch, mask2), dim=0)


        final_count = loaded_image_count

        return (final_image_batch, final_mask_batch, final_count)


NODE_CLASS_MAPPINGS = {
    "LoadBatchImagesDir": LoadBatchImagesDir,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadBatchImagesDir": "Load Batch From Dir (Creepybits)",
}

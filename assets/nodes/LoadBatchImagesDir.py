import os
import torch
from PIL import ImageOps
try:
    import pillow_jxl      # noqa: F401 - This import is for side-effect enabling JXL support in PIL, not directly used.
except ImportError:
    pass # JXL support won't be available if pillow_jxl isn't installed
import comfy.utils
from PIL import Image
import numpy as np


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
            # Include the folder's modification time so adding/removing images triggers a reload.
            directory = kwargs.get('directory', '')
            dir_mtime = os.path.getmtime(directory) if os.path.isdir(directory) else 0
            relevant_kwargs = {k: v for k, v in kwargs.items() if k in ['directory', 'image_load_cap', 'start_index', 'force_rescan']}
            return hash((frozenset(relevant_kwargs.items()), dir_mtime))


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

            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.jxl', '.gif', '.bmp', '.tiff', '.ico')
            image_files_potential = []

            for filename in dir_files:
                if filename.lower().endswith(valid_extensions):
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


        # Resize everything to the first image's size, then concatenate once.
        # (Concatenating inside the loop copied the whole batch on every image.)
        target_height, target_width = images[0].shape[1], images[0].shape[2]
        target_size = (target_height, target_width)

        for idx in range(1, len(images)):
            if images[idx].shape[1:3] != target_size:
                images[idx] = comfy.utils.common_upscale(
                    images[idx].movedim(-1, 1), target_width, target_height, "bilinear", "center"
                ).movedim(1, -1)
            if masks[idx].shape[1:3] != target_size:
                masks[idx] = torch.nn.functional.interpolate(
                    masks[idx].unsqueeze(1), size=target_size, mode='bilinear', align_corners=False
                ).squeeze(1)

        final_image_batch = torch.cat(images, dim=0)
        final_mask_batch = torch.cat(masks, dim=0)

        final_count = loaded_image_count

        return (final_image_batch, final_mask_batch, final_count)


NODE_CLASS_MAPPINGS = {
    "LoadBatchImagesDir": LoadBatchImagesDir,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadBatchImagesDir": "Load Batch Images From Dir (Creepybits)",
}

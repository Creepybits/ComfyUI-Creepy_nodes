# --- START OF FILE LoadBatchImagesDir.py ---

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
# from .libs.utils import ByPassTypeTuple, empty_pil_tensor, empty_latent # Make sure these are correctly imported if used
from PIL import Image
import numpy as np
import logging

# Configure logging (optional, but good practice)
# logging.basicConfig(level=logging.INFO) # Uncomment to see INFO level messages

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
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT")
    FUNCTION = "load_images"

    CATEGORY = "Creepybits/image"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        if 'load_always' in kwargs and kwargs['load_always']:
            return float("NaN")
        else:
            return hash(frozenset(kwargs))

    # --- Inside LoadBatchImagesDir class ---
    def load_images(self, directory: str, image_load_cap: int = 0, start_index: int = 0, load_always=False):
        print(f"LoadBatchImagesDir: Starting load_images for directory: {directory}")
        print(f"LoadBatchImagesDir: image_load_cap={image_load_cap}, start_index={start_index}, load_always={load_always}")

        if not os.path.isdir(directory):
            print(f"LoadBatchImagesDir ERROR: Directory '{directory}' not found.")
            raise FileNotFoundError(f"Directory '{directory} cannot be found.'")

        dir_files = os.listdir(directory)
        print(f"LoadBatchImagesDir: Found {len(dir_files)} files in directory.")

        if not dir_files:
            print(f"LoadBatchImagesDir ERROR: No files found in directory '{directory}'.")
            raise FileNotFoundError(f"No files in directory '{directory}'.")

        # More aggressive extension filtering (case-insensitive)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.jxl', '.gif', '.bmp', '.tiff', '.ico']
        image_files_potential = []

        for filename in dir_files:
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                full_path = os.path.join(directory, filename)
                try:
                    # Attempt to open and verify the image using PIL
                    with Image.open(full_path) as img:
                        img.verify()
                    image_files_potential.append(filename)
                    print(f"LoadBatchImagesDir: Validated image: {filename}")
                except (IOError, SyntaxError) as e:
                    print(f"LoadBatchImagesDir WARNING: Skipping file due to PIL error: {filename} - {e}")
                except Exception as e:
                    print(f"LoadBatchImagesDir WARNING: Skipping file: {filename} - {type(e).__name__} - {e}")
            else:
                print(f"LoadBatchImagesDir WARNING: Skipping file due to invalid extension: {filename}")


        if not image_files_potential:
            print(f"LoadBatchImagesDir ERROR: No valid images found in directory '{directory}' after filtering.")
            raise FileNotFoundError(f"No valid images found in directory '{directory}'.")

        # Filter and sort image files based on start_index and load_cap
        image_files_potential = sorted(image_files_potential)

        actual_start_index = start_index
        if start_index < 0 or start_index >= len(image_files_potential):
             print(f"LoadBatchImagesDir WARNING: start_index {start_index} is out of range ({len(image_files_potential)} files). Using 0.")
             actual_start_index = 0

        image_files_to_load = image_files_potential[actual_start_index:]

        if image_load_cap > 0:
             image_files_to_load = image_files_to_load[:image_load_cap]

        image_paths_to_load = [os.path.join(directory, x) for x in image_files_to_load]

        print(f"LoadBatchImagesDir: Identified {len(image_paths_to_load)} images to load after index/cap.")

        images = []
        masks = []
        loaded_image_count = 0

        for image_path in image_paths_to_load:
            try:
                with Image.open(image_path) as i:
                    i = ImageOps.exif_transpose(i)
                    # Process image
                    image = i.convert("RGB")
                    image = np.array(image).astype(np.float32) / 255.0
                    image = torch.from_numpy(image)[None,]  # Add batch dimension (1, H, W, 3)

                    # Process mask (Alpha channel or default opaque)
                    if 'A' in i.getbands():
                        mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                        mask = 1. - torch.from_numpy(mask) # Invert mask (transparency -> opacity)
                        mask = mask.unsqueeze(0) # Add batch dimension (1, H, W)
                    else:
                        # Create a default opaque mask (all 1s) if no alpha channel (1, H, W)
                        mask = torch.ones((image.shape[1], image.shape[2]), dtype=torch.float32, device="cpu").unsqueeze(0)


                    images.append(image)
                    masks.append(mask)
                    loaded_image_count += 1
                    print(f"LoadBatchImagesDir: Successfully loaded and processed image: {os.path.basename(image_path)}")
                    print(f"LoadBatchImagesDir: Loaded image shape: {image.shape}, mask shape: {mask.shape}")


            except Exception as e:
                print(f"LoadBatchImagesDir ERROR: Error processing image {os.path.basename(image_path)}: {e}")
                continue # Skip to the next file


        if not images:
            print(f"LoadBatchImagesDir ERROR: No images could be loaded from '{directory}' after processing.")
            raise FileNotFoundError(f"No images could be loaded from '{directory}'.")

        # --- Batching Logic ---
        print(f"LoadBatchImagesDir: Starting batching {len(images)} images/masks.")

        # Start the batches with the first image/mask
        image_batch = images[0] # Shape (1, H1, W1, 3)
        mask_batch = masks[0]   # Shape (1, H1, W1)

        print(f"LoadBatchImagesDir: Initial image batch shape: {image_batch.shape}, Mask batch shape: {mask_batch.shape}")

        for idx in range(1, len(images)):
            image2 = images[idx] # Shape (1, H2, W2, 3)
            mask2 = masks[idx]   # Shape (1, H2, W2)
            print(f"LoadBatchImagesDir: Processing item {idx+1}/{len(images)}. Current image shape: {image2.shape}, mask shape: {mask2.shape}")

            # Target dimensions for both image2 and mask2 are derived from the current batch dimensions
            target_height = image_batch.shape[1] # Height from image batch (or mask batch, should be same)
            target_width = image_batch.shape[2]  # Width from image batch (or mask batch, should be same)
            target_size = (target_height, target_width) # (H, W)

            # Upscale image if needed before concatenation
            if image2.shape[1:3] != target_size: # Check Height and Width
                print(f"LoadBatchImagesDir: Upscaling image {idx+1} from {image2.shape[1:3]} to match batch shape {target_size}")
                # Comfy's upscale needs channel first (B, C, H, W)
                image2_upscaled = comfy.utils.common_upscale(
                    image2.movedim(-1, 1), # Move channels to dim 1
                    target_width, # Target width first
                    target_height, # Target height second
                    "bilinear",
                    "center"
                ).movedim(1, -1) # Move channels back to last dim
                # Ensure upscaled image has the target size before concatenating (belt and suspenders check)
                if image2_upscaled.shape[1:3] != target_size:
                     print(f"LoadBatchImagesDir ERROR: Image upscaling failed to reach target size {target_size}. Got {image2_upscaled.shape[1:3]}")
                     # Decide how to handle: skip this image, raise error? For now, raise error.
                     raise RuntimeError(f"Image upscaling failed for {os.path.basename(image_paths_to_load[idx])}")
                image_batch = torch.cat((image_batch, image2_upscaled), dim=0)
                print(f"LoadBatchImagesDir: Image {idx+1} upscaled and concatenated. New batch shape: {image_batch.shape}")
            else:
                image_batch = torch.cat((image_batch, image2), dim=0)
                print(f"LoadBatchImagesDir: Image {idx+1} concatenated (no upscale). New batch shape: {image_batch.shape}")


            # Upscale mask if needed before concatenation
            # Masks are (1, H, W). Interpolate needs (N, C, H, W). Add a channel dim (size 1).
            # Target size for mask2 is the same as the image batch: (target_height, target_width)
            if mask2.shape[1:3] != target_size: # Check Height and Width
                print(f"LoadBatchImagesDir: Upscaling mask {idx+1} from {mask2.shape[1:3]} to match batch shape {target_size}")

                # Prepare mask for interpolate: (1, H, W) -> (1, 1, H, W)
                mask2_interp_input = mask2.unsqueeze(1)

                # Interpolate to the target height/width
                mask2_upscaled_interp = torch.nn.functional.interpolate(
                    mask2_interp_input,
                    size=target_size, # Target height, width
                    mode='bilinear',
                    align_corners=False
                )

                # Squeeze the channel dimension back to get (1, target_H, target_W)
                mask2_upscaled = mask2_upscaled_interp.squeeze(1) # Shape (1, target_H, target_W)

                # Ensure upscaled mask has the target size before concatenating (belt and suspenders check)
                if mask2_upscaled.shape[1:3] != target_size:
                     print(f"LoadBatchImagesDir ERROR: Mask upscaling failed to reach target size {target_size}. Got {mask2_upscaled.shape[1:3]}")
                     # Decide how to handle: skip this mask, raise error? For now, raise error.
                     raise RuntimeError(f"Mask upscaling failed for {os.path.basename(image_paths_to_load[idx])}")

                # Concatenate with the mask_batch (B, H, W)
                mask_batch = torch.cat((mask_batch, mask2_upscaled), dim=0)
                print(f"LoadBatchImagesDir: Mask {idx+1} upscaled and concatenated. New batch shape: {mask_batch.shape}")
            else:
                 # If shapes match, concatenate directly
                 mask_batch = torch.cat((mask_batch, mask2), dim=0)
                 print(f"LoadBatchImagesDir: Mask {idx+1} concatenated (no upscale). New batch shape: {mask_batch.shape}")


        final_image_batch = image_batch
        final_mask_batch = mask_batch
        final_count = loaded_image_count # Use the count of successfully loaded images

        print(f"LoadBatchImagesDir: Final image batch shape: {final_image_batch.shape}")
        print(f"LoadBatchImagesDir: Final mask batch shape: {final_mask_batch.shape}")
        print(f"LoadBatchImagesDir: Final count: {final_count}")
        print(f"LoadBatchImagesDir: Returning (image_batch, mask_batch, count)")

        return (final_image_batch, final_mask_batch, final_count)

# ... rest of the file (NODE_CLASS_MAPPINGS, etc.) ...

# NOTE: Ensure ByPassTypeTuple etc. from libs.utils are available or remove/replace if not used.
# If you removed them from your actual file, you should also remove the import.


NODE_CLASS_MAPPINGS = {
    "LoadBatchImagesDir": LoadBatchImagesDir,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadBatchImagesDir": "Load Batch From Dir (Creepybits)",
}

# --- END OF FILE LoadBatchImagesDir.py ---

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
from .libs.utils import ByPassTypeTuple, empty_pil_tensor, empty_latent
from PIL import Image
import numpy as np
import logging


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

    def load_images(self, directory: str, image_load_cap: int = 0, start_index: int = 0, load_always=False):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory} cannot be found.'")

        dir_files = os.listdir(directory)
        if not dir_files:
            raise FileNotFoundError(f"No files in directory '{directory}'.")

        # More aggressive extension filtering (case-insensitive)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.jxl', '.gif', '.bmp', '.tiff', '.ico']  # Added more extensions
        image_files = []

        for filename in dir_files:
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                full_path = os.path.join(directory, filename)
                try:
                    # Attempt to open and verify the image
                    img = Image.open(full_path)
                    img.verify()  # Verify that it is, in fact, an image
                    img = ImageOps.exif_transpose(img)  # Orient based on EXIF data
                    image_files.append(filename)
                    logging.info(f"Successfully validated image: {filename}")
                except (IOError, SyntaxError) as e:
                    logging.warning(f"Skipping file due to PIL error: {filename} - {e}")
                except Exception as e:
                    logging.warning(f"Skipping file: {filename} - {type(e).__name__} - {e}")
            else:
                logging.warning(f"Skipping file due to invalid extension: {filename}")

        if not image_files:
            raise FileNotFoundError(f"No valid images found in directory '{directory}'.")

        # start at start_index
        image_files = sorted(image_files)  # Sort the image files
        image_files = [os.path.join(directory, x) for x in image_files]  # Create full paths


        images = []
        masks = []

        limit_images = False
        if image_load_cap > 0:
            limit_images = True
        image_count = 0

        has_non_empty_mask = False

        for image_path in image_files:
            if limit_images and image_count >= image_load_cap:
                break

            try:
                i = Image.open(image_path)
                i = ImageOps.exif_transpose(i)
                image = i.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]  # Add batch dimension here

                if 'A' in i.getbands():
                    mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                    mask = 1. - torch.from_numpy(mask)
                    has_non_empty_mask = True
                    # Ensure mask is 3D (batch dimension)
                    mask = mask.unsqueeze(0)
                else:
                    # Create a 2D mask and unsqueeze it.
                    mask = torch.zeros((i.size[1], i.size[0]), dtype=torch.float32, device="cpu") #Height, Width
                    mask = mask.unsqueeze(0)  # Add batch dimension here (makes it 3D)

                images.append(image)
                masks.append(mask)
                image_count += 1

            except Exception as e:
                logging.error(f"Error processing image {image_path}: {e}")
                continue  # Skip to the next file

        if not images:
            raise FileNotFoundError(f"No images could be loaded from '{directory}'.")

        if len(images) == 1:
            return (images[0], masks[0], 1)

        image1 = images[0]
        mask1 = masks[0]

        for image2, mask2 in zip(images[1:], masks[1:]):
            if image1.shape[1:] != image2.shape[1:]:
                image2 = comfy.utils.common_upscale(image2.movedim(-1, 1), image1.shape[2], image1.shape[1], "bilinear", "center").movedim(1, -1)

            image1 = torch.cat((image1, image2), dim=0)

            #Corrected upscaling logic
            if mask1.shape[1:] != mask2.shape[1:]:
                print(f"Shape Mask1 {mask1.shape}")
                print(f"Shape Mask2 {mask2.shape}")
                mask2 = torch.nn.functional.interpolate(mask2.unsqueeze(0), size=(image1.shape[1], image1.shape[2]), mode='bilinear', align_corners=False)

        print(f"Shape Mask1: {mask1.shape}")
        print(f"Shape Mask2: {mask2.shape}")
            # Check the shapes of mask1 and mask2 just before concatenation
        if len(mask1.shape) != len(mask2.shape):
            print("Masks have different dimensions!")
            # Add dimensions to whichever mask is missing one
            if len(mask1.shape) < len(mask2.shape):
                mask1 = mask1.unsqueeze(1)
            else:
                mask2 = mask2.unsqueeze(1)

        mask1 = torch.cat((mask1, mask2), dim=0)


        return (image1, mask1, len(images))

NODE_CLASS_MAPPINGS = {  # <---Outdent these lines
    "LoadBatchImagesDir": LoadBatchImagesDir,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadBatchImagesDir": "Load Batch From Dir (Creepybits)",
}

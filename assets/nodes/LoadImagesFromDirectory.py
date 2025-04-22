from PIL import Image
import torch
import numpy as np
import os
import random

class LoadImagesFromDirectory:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "randomize": ("BOOLEAN", {"default": False}),
                "image_load_cap": ("INT", {"default": 10, "min": 1, "max": 100}),
                "target_width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "target_height": ("INT", {"default": 512, "min": 64, "max": 2048}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "load_images"
    CATEGORY = "Creepybits/Image"

    def load_images(self, directory, randomize, image_load_cap, target_width, target_height):
        image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]

        if randomize:
            random.shuffle(image_files)

        images = []
        for image_file in image_files[:image_load_cap]:
            image_path = os.path.join(directory, image_file)
            try:
                i = Image.open(image_path)
                i = i.convert("RGB")
                i = i.resize((target_width, target_height)) # Resize the image

                image = i.copy()
                i.close()
                image = torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)
                images.append(image)
            except Exception as e:
                print(f"Error loading image: {image_path}, error: {e}")

        if not images:
            print(f"No images loaded from directory: {directory}")
            return (torch.zeros([1,target_height,target_width,3]),)  # Return a black image

        return (torch.cat(images, dim=0),)

NODE_CLASS_MAPPINGS = {
    "LoadImagesFromDirectory": LoadImagesFromDirectory,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagesFromDirectory": "Load Images From Directory (Creepybits)",
}

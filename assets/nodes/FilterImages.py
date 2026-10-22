import os
from PIL import Image


def is_image(filepath):
    # imghdr was removed from Python 3.13; Pillow recognises more formats anyway.
    try:
        with Image.open(filepath) as img:
            img.verify()
        return True
    except Exception:
        return False


class FilterImages:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"folder_path": ("STRING", {"default": ""}), }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_paths",)
    OUTPUT_NODE = True
    CATEGORY = "Creepybits/utilities"
    FUNCTION = "filter_images"

    def filter_images(self, folder_path):
        if not os.path.isdir(folder_path):
            print(f"Error: '{folder_path}' is not a valid directory.")
            return ("",)

        image_paths = []
        for entry in sorted(os.scandir(folder_path), key=lambda e: e.name):
            if entry.is_file() and is_image(entry.path):
                image_paths.append(entry.path)

        # STRING outputs must be a string; one path per line.
        return ("\n".join(image_paths),)


NODE_CLASS_MAPPINGS = {
    "FilterImages": FilterImages
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FilterImages": "Filter Image Paths (Creepybits)"
}

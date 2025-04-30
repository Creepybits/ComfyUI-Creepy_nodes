import os
import imghdr

class FilterImages:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"folder_path": ("STRING", {"default": ""}), }}

    RETURN_TYPES = ("STRING",)  # Returns a list of image file paths
    RETURN_NAMES = ("image_paths",)
    OUTPUT_NODE = True
    CATEGORY = "Creepybits/utilities"

    def filter_images(self, folder_path):
        if not os.path.isdir(folder_path):
            print(f"Error: '{folder_path}' is not a valid directory.")
            return ([],)  # Return an empty list if the folder is invalid

        image_paths = []
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath) and imghdr.what(filepath) is not None:  # imghdr checks if the file is an image
                image_paths.append(filepath)

        return (image_paths,)

    FUNCTION = "filter_images"

NODE_CLASS_MAPPINGS = {
    "FilterImages": FilterImages
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FilterImages": "Filter Image Paths (Creepybits)"
}

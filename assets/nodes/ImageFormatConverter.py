import os
from PIL import Image

# Make sure Pillow is installed. It's usually a dependency of ComfyUI.
# If not, run: pip install Pillow

class ImageFormatConverter:
    """
    A ComfyUI node to batch-convert images in a folder from one format to another.
    This node recursively scans all subdirectories.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source_folder": ("STRING", {"multiline": True, "default": "C:\\path\\to\\your\\images"}),
                "source_formats": ("STRING", {"multiline": False, "default": "png, jpg, jpeg"}),
                "target_format": (['webp', 'png', 'jpg', 'jpeg', 'bmp'],),
                "quality": ("INT", {"default": 85, "min": 1, "max": 100, "step": 1}),
                "delete_original": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "convert_images"
    CATEGORY = "Creepybits/Utilities"

    def convert_images(self, source_folder, source_formats, target_format, quality, delete_original):
        if not os.path.isdir(source_folder):
            return (f"Error: Source folder '{source_folder}' does not exist.",)

        # Normalize source formats into a list of lowercase extensions without dots
        source_exts = [f.strip().lower().replace('.', '') for f in source_formats.split(',')]
        target_ext = target_format.lower().replace('.', '')

        converted_count = 0
        skipped_count = 0
        error_count = 0

        print(f"[Creepy_ImageConverter] Starting conversion in '{source_folder}'...")

        for root, _, files in os.walk(source_folder):
            for file in files:
                try:
                    file_name, file_ext = os.path.splitext(file)
                    file_ext_clean = file_ext.lower().replace('.', '')

                    if file_ext_clean in source_exts:
                        source_path = os.path.join(root, file)
                        dest_path = os.path.join(root, f"{file_name}.{target_ext}")

                        if source_path == dest_path:
                            skipped_count += 1
                            continue

                        with Image.open(source_path) as img:
                            # Handle transparency for JPG conversion
                            if target_ext in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                                img = img.convert("RGB")

                            # Save with quality settings if applicable
                            if target_ext in ['jpg', 'jpeg', 'webp']:
                                img.save(dest_path, format=target_ext, quality=quality)
                            else:
                                img.save(dest_path, format=target_ext)

                        converted_count += 1

                        if delete_original:
                            os.remove(source_path)

                except Exception as e:
                    print(f"[Creepy_ImageConverter] Error converting file '{file}': {e}")
                    error_count += 1

        status_message = (
            f"Conversion complete.\n"
            f"Converted: {converted_count}\n"
            f"Skipped (same format): {skipped_count}\n"
            f"Errors: {error_count}"
        )
        print(f"[Creepy_ImageConverter] {status_message.replace(chr(10), ' ')}")

        return (status_message,)


# Node Mappings
NODE_CLASS_MAPPINGS = {
    "ImageFormatConverter": ImageFormatConverter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageFormatConverter": "Image Format Converter (Creepybits)",
}

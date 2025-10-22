import os
import shutil
# --- ADDED ---
# defaultdict is perfect for counting items in categories without checking if the key exists first.
from collections import defaultdict

class FileSorterNode:
    """
    A ComfyUI node to sort files in a directory into subfolders based on their extension.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_folder": ("STRING", {"default": "C:\\ComfyUI\\output\\", "multiline": False}),
                "image_extensions": ("STRING", {"default": ".png, .jpg, .jpeg, .webp, .gif, .bmp", "multiline": True}),
                "video_extensions": ("STRING", {"default": ".mp4, .mov, .avi, .mkv, .webm", "multiline": True}),
                "execute_sort": ("BOOLEAN", {"default": False}), # Safety first!
            },
            "optional": {
                 "other_mappings": ("STRING", {"default": "Audio:.mp3,.wav,.flac\nDocs:.txt,.md", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("status", "files_moved_count",)
    FUNCTION = "sort_files"
    CATEGORY = "Creepybits/FileIO"

    def sort_files(self, target_folder, image_extensions, video_extensions, execute_sort, other_mappings=""):
        # --- REFACTORED: The initial execute_sort check is removed from here ---

        if not os.path.isdir(target_folder):
            error_message = f"Error: The directory '{target_folder}' does not exist."
            print(error_message)
            return (error_message, 0)

        # --- Build the extension-to-folder mapping (This logic is unchanged) ---
        mapping = {}
        def process_ext_string(ext_string, folder_name, a_mapping):
            extensions = {ext.strip().lower() for ext in ext_string.split(',') if ext.strip()}
            for ext in extensions:
                a_mapping[ext] = folder_name

        process_ext_string(image_extensions, "Images", mapping)
        process_ext_string(video_extensions, "Videos", mapping)

        if other_mappings:
            for line in other_mappings.split('\n'):
                if ':' in line:
                    folder_part, exts_part = line.split(':', 1)
                    process_ext_string(exts_part, folder_part.strip(), mapping)

        # --- REFACTORED: We now scan first, then decide to act. ---

        # This dictionary will hold the counts for our dry run report.
        files_to_sort_by_category = defaultdict(int)

        # We'll create a list of files to process to avoid iterating the directory twice.
        files_to_process = []

        for filename in os.listdir(target_folder):
            source_path = os.path.join(target_folder, filename)
            if not os.path.isfile(source_path):
                continue

            file_ext = os.path.splitext(filename)[1].lower()
            target_subfolder = mapping.get(file_ext)

            if not target_subfolder and file_ext:
                 target_subfolder = file_ext[1:].upper()

            if target_subfolder:
                # If a file has a destination, we add it to our list and count it.
                files_to_process.append((filename, source_path, target_subfolder))
                files_to_sort_by_category[target_subfolder] += 1

        total_files_to_move = len(files_to_process)

        # --- Decision Point: Are we doing a real run or just a dry run? ---

        if execute_sort:
            # --- REAL RUN LOGIC ---
            print("-" * 50)
            print(f"Executing sort in '{target_folder}'...")
            files_moved = 0
            for filename, source_path, target_subfolder in files_to_process:
                dest_dir = os.path.join(target_folder, target_subfolder)
                dest_path = os.path.join(dest_dir, filename)

                try:
                    os.makedirs(dest_dir, exist_ok=True)
                    print(f"Moving '{filename}' to '{target_subfolder}\\'")
                    shutil.move(source_path, dest_path)
                    files_moved += 1
                except Exception as e:
                    print(f"ERROR: Could not move {filename}. Reason: {e}")

            summary = f"Sorting complete. Moved {files_moved} file(s)."
            print(summary)
            print("-" * 50)
            return (summary, files_moved)

        else:
            # --- DRY RUN LOGIC ---
            if total_files_to_move == 0:
                return ("No files found that matched the sorting criteria.", 0)

            report_lines = ["[DRY RUN]"]
            report_lines.append("Found the following files to sort:")
            # Sort the dictionary by category name for a consistent, clean report
            for category, count in sorted(files_to_sort_by_category.items()):
                report_lines.append(f"- {category}: {count} file(s)")

            report_lines.append("") # Add a blank line for readability
            report_lines.append(f"Set 'execute_sort' to True to move {total_files_to_move} file(s).")

            dry_run_summary = "\n".join(report_lines)
            return (dry_run_summary, total_files_to_move)


# These mappings remain unchanged
NODE_CLASS_MAPPINGS = {
    "FileSorterNode": FileSorterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FileSorterNode": "File Sorter (Creepybits)"
}

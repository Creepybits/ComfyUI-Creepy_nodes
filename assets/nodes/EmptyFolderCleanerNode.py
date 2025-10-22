import os
import folder_paths

class EmptyFolderCleanerNode:
    """
    A ComfyUI node to recursively delete empty folders within a specified directory.
    Now with a 'dry run' preview feature!
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_folder": ("STRING", {"default": "C:\\path\\to\\output_folder", "multiline": False}),
                "execute_cleanup": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("status", "folder_count",)
    FUNCTION = "cleanup_folders"
    CATEGORY = "Creepybits_Utils/FileIO"

    def cleanup_folders(self, target_folder, execute_cleanup):
        # --- Path Validation (run for both modes) ---
        if not os.path.isdir(target_folder):
            error_message = f"Error: The directory '{target_folder}' was not found."
            print(error_message)
            return (error_message, 0)

        # --- Combined Scanning & Cleanup Logic ---
        print("-" * 50)
        mode_str = "Cleaning up" if execute_cleanup else "DRY RUN: Scanning"
        print(f"{mode_str} empty folders in '{target_folder}'...")

        folders_processed_count = 0

        try:
            # We walk from the bottom up to handle nested empty folders correctly
            for dirpath, dirnames, filenames in os.walk(target_folder, topdown=False):
                if not dirnames and not filenames:
                    # This is an empty folder, so we always count it
                    folders_processed_count += 1

                    # But we only DELETE it if execute_cleanup is True
                    if execute_cleanup:
                        try:
                            print(f"Deleting empty folder: {dirpath}")
                            os.rmdir(dirpath)
                        except OSError as e:
                            print(f"Error deleting {dirpath}: {e}")
                    else:
                        # In dry run mode, we just log what we found
                        print(f"Preview: Found empty folder: {dirpath}")

        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)
            return (error_message, folders_processed_count)

        # --- Dynamic Summary Message ---
        if execute_cleanup:
            if folders_processed_count > 0:
                summary = f"Cleanup complete! Successfully deleted {folders_processed_count} empty folder(s)."
            else:
                summary = "Cleanup complete. No empty folders were found to delete."
        else:
            summary = f"DRY RUN: Found {folders_processed_count} empty folder(s) that can be deleted. Set 'execute_cleanup' to True to proceed."

        print(summary)
        print("-" * 50)

        return (summary, folders_processed_count)


NODE_CLASS_MAPPINGS = {
    "EmptyFolderCleaner": EmptyFolderCleanerNode # Add this line
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EmptyFolderCleaner": "Empty Folder Cleaner (Creepybits)" # Add this line
}

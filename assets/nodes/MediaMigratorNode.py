import os
import shutil
import folder_paths

class MediaMigratorNode:
    """
    A ComfyUI node to move media files from a source folder to a destination,
    preserving the directory structure. Now with a 'dry run' preview feature!
    """
    # --- CONFIGURATION ---
    CONTAINER_FOLDER_NAME = "_Moved_media"
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff'}
    VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'}
    MEDIA_EXTENSIONS = IMAGE_EXTENSIONS.union(VIDEO_EXTENSIONS)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source_folder": ("STRING", {"default": "C:\\path\\to\\source", "multiline": False}),
                "destination_drive": ("STRING", {"default": "D:\\", "multiline": False}),
                "execute_move": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "execute_migration"
    CATEGORY = "Creepybits_Utils/FileIO" # Adjusted to match your pack

    def execute_migration(self, source_folder, destination_drive, execute_move):
        # --- Safety Checks (run for both modes) ---
        if not os.path.isdir(source_folder):
            error_message = f"ERROR: Source folder '{source_folder}' does not exist. Aborting."
            print(error_message)
            return (error_message,)

        if not os.path.isdir(destination_drive):
            error_message = f"ERROR: Destination drive '{destination_drive}' does not exist. Aborting."
            print(error_message)
            return (error_message,)

        source_drive = os.path.splitdrive(source_folder)[0]
        dest_drive_letter = os.path.splitdrive(destination_drive)[0]
        if source_drive.lower() == dest_drive_letter.lower():
            if os.path.commonpath([source_folder, destination_drive]) == source_folder:
                error_message = "ERROR: The destination cannot be inside the source folder. Aborting."
                print(error_message)
                return (error_message,)

        final_destination_root = os.path.join(destination_drive, self.CONTAINER_FOLDER_NAME)

        # --- NEW: Combined Scanning Logic ---
        print("-" * 50)
        mode_str = "Scanning" if execute_move else "DRY RUN: Scanning"
        print(f"{mode_str} '{source_folder}' for media files...")

        total_files_found = 0
        total_space_found = 0

        # We walk the directory tree for both the dry run and the actual move
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in self.MEDIA_EXTENSIONS:
                    source_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(source_path)
                        total_files_found += 1
                        total_space_found += file_size

                        # The critical part: ONLY perform disk operations if execute_move is True
                        if execute_move:
                            relative_path = os.path.relpath(root, source_folder)
                            dest_dir = os.path.join(final_destination_root, relative_path)
                            os.makedirs(dest_dir, exist_ok=True)
                            dest_path = os.path.join(dest_dir, file)

                            print(f"Moving: {file} ({file_size / 1024 / 1024:.2f} MB)")
                            shutil.move(source_path, dest_path)

                    except Exception as e:
                        # Log errors in both modes
                        error_log = f"ERROR: Could not process {source_path}. Reason: {e}"
                        print(error_log)

        # --- NEW: Dynamic Summary Message ---
        space_in_mb = total_space_found / 1024 / 1024
        if execute_move:
            summary = f"Migration complete! Moved {total_files_found} files, clearing {space_in_mb:.2f} MB."
        else:
            summary = f"DRY RUN: Found {total_files_found} media files, totaling {space_in_mb:.2f} MB. Set 'execute_move' to True to proceed."

        print(summary)
        print("-" * 50)

        return (summary,)


# --- Node Mappings ---
# This is how ComfyUI finds your node.
NODE_CLASS_MAPPINGS = {
    "MediaMigratorNode": MediaMigratorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MediaMigratorNode": "Media File Migrator (Creepybits)"
}

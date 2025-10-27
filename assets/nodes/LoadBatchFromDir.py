import os
import random
import torch
import numpy as np
from PIL import Image, PngImagePlugin
import json

class LoadBatchFromDir:
    _state_file_path = os.path.join(os.path.expanduser("~"), ".creepybits_loader_state.json")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": "C:/path/to/your/images"}),
                "iteration_mode": (["fixed", "increment", "random"],),
            },
            # --- The NEW, Optional Input ---
            # This is our "poker". It doesn't do anything inside the code,
            # but connecting a changing value to it will force a re-run.
            "optional": {
                "trigger": ("*",)
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "INT")
    RETURN_NAMES = ("IMAGE", "MASK", "current_index")
    FUNCTION = "load_one_from_dir_persistent"
    CATEGORY = "Creepybits/Loaders"

    def _load_state(self):
        if not os.path.exists(self._state_file_path): return {}
        try:
            with open(self._state_file_path, 'r') as f: return json.load(f)
        except (json.JSONDecodeError, IOError): return {}

    def _save_state(self, state_dict):
        try:
            os.makedirs(os.path.dirname(self._state_file_path), exist_ok=True)
            with open(self._state_file_path, 'w') as f: json.dump(state_dict, f, indent=4)
        except IOError: print(f"Warning: Could not save state to {self._state_file_path}")

    # Note: the 'trigger' argument is accepted but intentionally not used inside the function.
    def load_one_from_dir_persistent(self, directory, iteration_mode, trigger=None):
        if not os.path.isdir(directory): raise FileNotFoundError(f"Directory not found: {directory}")

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', 'webp']
        files = sorted([f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in image_extensions])

        if not files: raise FileNotFoundError(f"No image files found in directory: {directory}")

        num_files = len(files)

        # We need a start index. Let's default to 0 if not specified elsewhere.
        start_index = 0
        current_index = 0
        image_load_cap = 1 # We are hardcoding to 1 since we only load one image.

        if iteration_mode == "increment":
            all_states = self._load_state()
            current_index = all_states.get(directory, start_index)
            all_states[directory] = current_index + image_load_cap
            self._save_state(all_states)
        elif iteration_mode == "fixed":
            # In fixed mode, we might want to respect some external input if we had one.
            # For now, we'll assume it starts at 0 unless we add a start_index widget back.
            current_index = start_index
        elif iteration_mode == "random":
            current_index = random.randint(0, num_files - 1)

        current_index = current_index % num_files

        selected_file = files[current_index]
        image_path = os.path.join(directory, selected_file)
        img = Image.open(image_path)

        if 'A' in img.getbands():
            mask = np.array(img.getchannel('A')).astype(np.float32) / 255.0
            mask_tensor = torch.from_numpy(mask)
        else:
            mask_tensor = torch.ones((img.height, img.width), dtype=torch.float32)

        img = img.convert("RGB")
        image_np = np.array(img).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np).unsqueeze(0)
        final_mask = mask_tensor.unsqueeze(0)

        return (image_tensor, final_mask, current_index)


NODE_CLASS_MAPPINGS = {
    "LoadBatchFromDir": LoadBatchFromDir,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadBatchFromDir": "Load Batch From Dir (Creepybits)",
}

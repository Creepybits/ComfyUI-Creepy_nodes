import os
import folder_paths # ComfyUI utility for finding paths
# import comfy.sd # Not strictly needed if using LoraLoader directly
# import comfy.utils # Not strictly needed if using LoraLoader directly

from nodes import LoraLoader # Using ComfyUI's built-in LoraLoader

# Helper function to get filenames recursively within a ComfyUI models subdirectory
def get_recursive_filenames(folder_name):
    full_path_dir = folder_paths.get_folder_paths(folder_name)
    if not full_path_dir:
        return []

    filenames = []
    for base_dir in full_path_dir:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                filenames.append(relative_path.replace("\\", "/")) # Ensure forward slashes for consistency
    return filenames

class ConditionalLoRAApplierCreepybits:
    def __init__(self):
        # Instantiate LoraLoader once if it's stateless, or per-execution if it manages state.
        # It's usually safer to instantiate per-execution or ensure it's stateless.
        # For simplicity and robustnes, we'll instantiate it inside apply_conditional_lora.
        pass

    @classmethod
    def INPUT_TYPES(s):
        lora_list = get_recursive_filenames("loras")
        lora_names = ["None"] + [l for l in lora_list if l.lower().endswith((".safetensors", ".ckpt"))]
        lora_names.sort(key=lambda x: x.lower()) # Sort for better readability in dropdown

        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "lora_definitions": ("STRING", {
                    "multiline": True,
                    "default": """
# Define your LoRA rules here.
# Format: keyword_phrase_1, keyword_phrase_2, ... : lora_full_relative_path, lora_strength, clip_strength
# If ANY of the comma-separated keyword phrases are found in the prompt, the LoRA will be applied.
# Example (use forward slashes for paths):
# portrait, face detail: Flux/Details/amateur_photo_v1.safetensors, 0.75, 1.0
# cinematic scene, movie shot: MyLoRAs/Styles/retro_cinematic_v2.safetensors, 0.8, 0.9
# fantasy creature, mythical beast: Custom/Creatures/mythic_beast_lora.safetensors, 0.9, 0.9
# Use comma-separated values for strength. Default is 1.0 if omitted.
# Keep strength between -2.0 and 2.0.
# All keyword_phrases should be found anywhere in the prompt (case-insensitive by default).
"""
                }),
            },
            "optional": {
                "default_lora_name": (lora_names, {"default": "None"}),
                "default_lora_strength": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "default_clip_strength": ("FLOAT", {"default": 1.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "case_sensitive": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP",)
    RETURN_NAMES = ("MODEL", "CLIP",)

    FUNCTION = "apply_conditional_lora"
    CATEGORY = "Creepybits/Model Patcher"

    def apply_conditional_lora(self, model, clip, prompt, lora_definitions, default_lora_name, default_lora_strength, default_clip_strength, case_sensitive):
        loras_to_apply = [] # List to store (filename, model_strength, clip_strength) for all matches

        processed_prompt = prompt if case_sensitive else prompt.lower()

        rules = lora_definitions.strip().split('\n')
        for rule_line in rules:
            rule_line = rule_line.strip()
            if not rule_line or rule_line.startswith('#'):
                continue

            try:
                parts = rule_line.split(':', 1)
                if len(parts) < 2:
                    print(f"Warning: Malformed LoRA rule (missing colon): '{rule_line}'")
                    continue

                # --- NEW PARSING FOR MULTIPLE KEYWORDS ---
                keyword_string = parts[0].strip()
                # Split the keyword string by commas to get individual keywords
                keywords_for_this_lora = [k.strip() for k in keyword_string.split(',')]
                if not case_sensitive:
                    keywords_for_this_lora = [k.lower() for k in keywords_for_this_lora]
                # --- END NEW PARSING ---

                lora_info_str = parts[1].strip()

                # Check if ANY of the keywords for this LoRA are present in the positive prompt
                match_found = False
                for kw in keywords_for_this_lora:
                    if kw in processed_prompt: # processed_prompt is already lowercased if not case_sensitive
                        match_found = True
                        break # Found a match, no need to check other keywords for this LoRA
                
                if match_found: # <--- Changed this condition
                    lora_details = [x.strip() for x in lora_info_str.split(',', 2)]

                    filename = lora_details[0]
                    strength = float(lora_details[1]) if len(lora_details) > 1 else 1.0
                    clip_strength = float(lora_details[2]) if len(lora_details) > 2 else 1.0

                    # Validate filename against available loras (recursively)
                    # Note: folder_paths.get_full_path will also validate if the file exists
                    # This pre-check helps provide clearer error messages early.
                    if folder_paths.get_full_path("loras", filename) is None:
                        print(f"Warning: LoRA file '{filename}' not found in 'loras' directory (or subdirectories) for rule '{rule_line}'. Skipping this rule.")
                        continue

                    # If a match is found and validated, add it to the list
                    loras_to_apply.append((filename, strength, clip_strength))

            except ValueError as e:
                print(f"Warning: Error parsing LoRA rule '{rule_line}': {e}. Skipping.")
            except Exception as e:
                print(f"An unexpected error occurred while parsing rule '{rule_line}': {e}. Skipping.")

        # --- LoRA Application Logic ---
        final_model = model
        final_clip = clip

        if not loras_to_apply: # If no rules matched, consider the default LoRA
            if default_lora_name and default_lora_name != "None":
                # Ensure the default LoRA exists before attempting to apply
                if folder_paths.get_full_path("loras", default_lora_name) is None:
                    print(f"Warning: Default LoRA file '{default_lora_name}' not found. Skipping default LoRA application.")
                else:
                    loras_to_apply.append((default_lora_name, default_lora_strength, default_clip_strength))

        if not loras_to_apply: # If still no LoRAs to apply, return original model/clip
            print("No LoRA selected or found for the given prompt/rules/default. Returning original model and clip.")
            return (final_model, final_clip,)

        # Instantiate LoraLoader here to avoid issues with its internal state if apply_conditional_lora is called multiple times
        lora_loader_instance = LoraLoader()

        # Apply all collected LoRAs sequentially
        for lora_filename, lora_strength, clip_strength in loras_to_apply:
            print(f"Attempting to apply LoRA: {lora_filename} (model_strength={lora_strength}, clip_strength={clip_strength}) based on prompt.")

            try:
                # Use LoraLoader's load_lora function directly.
                # It handles finding the file, loading it, and patching the model/clip.
                final_model, final_clip = lora_loader_instance.load_lora(
                    model=final_model, 
                    clip=final_clip, 
                    lora_name=lora_filename, # This is the full path relative to /models/loras or a known folder_paths entry
                    strength_model=lora_strength, 
                    strength_clip=clip_strength
                )
                
                print(f"Successfully applied LoRA: {lora_filename}")
            except Exception as e:
                print(f"FATAL ERROR applying LoRA '{lora_filename}': {e}. Skipping this LoRA.")
                # Do NOT return here, continue to apply other LoRAs if possible or just return current state

        return (final_model, final_clip,)

NODE_CLASS_MAPPINGS = {
    "ConditionalLoRAApplierCreepybits": ConditionalLoRAApplierCreepybits
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ConditionalLoRAApplierCreepybits": "Conditional LoRA Applier (Creepybits)"
}
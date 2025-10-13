import os
import json
import hashlib
import requests
import folder_paths

# --- Helper Functions ---

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def get_civitai_model_info_by_hash(hash_value):
    api_url = f"https://civitai.com/api/v1/model-versions/by-hash/{hash_value}"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Civitai API request failed: {e}")
    return None

# --- Get a list of all LoRA files for the dropdown ---
# This part is fine, as it already scans subdirectories for the list.
lora_paths = folder_paths.get_filename_list("loras")
lora_files = [os.path.basename(x) for x in lora_paths if x is not None]
lora_files.insert(0, "None")


class LoraDBBuilder:
    JSON_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Lora_db', 'lora_triggers.json')

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "lora_name": (lora_files,), "force_fetch": ("BOOLEAN", {"default": False}), }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("found_trigger_words",)
    FUNCTION = "build_database"
    CATEGORY = "Creepybits/Database"

    # THIS IS THE NEW, SMARTER PATH FINDING FUNCTION
    def find_lora_path_recursive(self, lora_name):
        loras_dir = folder_paths.get_folder_paths("loras")[0]
        for root, dirs, files in os.walk(loras_dir):
            if lora_name in files:
                return os.path.join(root, lora_name)
        return None

    def build_database(self, lora_name, force_fetch):
        output_triggers_str = ""
        if lora_name == "None": return ("",)

        lora_database = {}
        try:
            with open(self.JSON_FILE_PATH, 'r', encoding='utf-8') as f: lora_database = json.load(f)
        except Exception: pass # Ignore if file not found or corrupted, we'll create/overwrite it

        if lora_name not in lora_database or force_fetch:
            print(f"LoraDBBuilder: Fetching info for '{lora_name}'...")

            # USE THE NEW RECURSIVE SEARCH FUNCTION
            lora_path = self.find_lora_path_recursive(lora_name)

            if not lora_path:
                print(f"LoraDBBuilder ERROR: Could not find path for LoRA '{lora_name}' in any subfolder.")
                return ("",)

            lora_hash = calculate_sha256(lora_path)
            print(f"LoraDBBuilder: Calculated SHA256: {lora_hash}")
            model_info = get_civitai_model_info_by_hash(lora_hash)

            found_triggers = []
            if model_info and "trainedWords" in model_info and model_info["trainedWords"]:
                found_triggers = model_info["trainedWords"]
                print(f"LoraDBBuilder: Success! Found triggers from Civitai: {found_triggers}")
            else:
                print(f"LoraDBBuilder: No trigger words found on Civitai for this hash.")

            lora_database[lora_name] = found_triggers

            try:
                os.makedirs(os.path.dirname(self.JSON_FILE_PATH), exist_ok=True)
                with open(self.JSON_FILE_PATH, 'w', encoding='utf-8') as f: json.dump(lora_database, f, indent=4)
                print(f"LoraDBBuilder: Database updated and saved.")
            except Exception as e:
                print(f"LoraDBBuilder ERROR: Could not save database file. Reason: {e}")

        final_triggers = lora_database.get(lora_name, [])
        if final_triggers:
            output_triggers_str = ", ".join(final_triggers)

        return (output_triggers_str,)



# --- MAPPINGS ---
NODE_CLASS_MAPPINGS = {
    "LoraDBBuilder": LoraDBBuilder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraDBBuilder": "LoRA DB Builder (Creepybits)",
}

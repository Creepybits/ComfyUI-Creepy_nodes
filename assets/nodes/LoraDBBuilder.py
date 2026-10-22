import hashlib
import requests

from .libs.lora_utils import LORA_DB_PATH, lora_dropdown, find_lora_path, load_lora_db, save_lora_db

# --- Helper Functions ---

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):  # 1 MB chunks: LoRAs are hundreds of MB
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


class LoraDBBuilder:
    JSON_FILE_PATH = LORA_DB_PATH

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "lora_name": (lora_dropdown(),), "force_fetch": ("BOOLEAN", {"default": False}), }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("found_trigger_words",)
    FUNCTION = "build_database"
    CATEGORY = "Creepybits/Database"

    def build_database(self, lora_name, force_fetch):
        output_triggers_str = ""
        if lora_name == "None": return ("",)

        lora_database = {}
        try:
            lora_database = load_lora_db()
        except Exception: pass # Ignore if file not found or corrupted, we'll create/overwrite it

        if lora_name not in lora_database or force_fetch:
            print(f"LoraDBBuilder: Fetching info for '{lora_name}'...")

            lora_path = find_lora_path(lora_name)

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
                save_lora_db(lora_database)
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

import os
import json
import folder_paths

LORA_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'Lora_db', 'lora_triggers.json')


def lora_dropdown():
    """LoRA file names (without subfolders, which is how the trigger database is keyed).
    Built on each request, so new LoRAs show up after a refresh instead of a restart.
    folder_paths caches the directory scan itself, so this is cheap."""
    names = sorted({os.path.basename(x) for x in folder_paths.get_filename_list("loras") if x})
    return ["None"] + names


def find_lora_path(lora_name):
    """Full path of a LoRA given only its file name, searching every configured LoRA folder."""
    for relative_path in folder_paths.get_filename_list("loras"):
        if os.path.basename(relative_path) == lora_name:
            return folder_paths.get_full_path("loras", relative_path)
    return None


def load_lora_db():
    with open(LORA_DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_lora_db(lora_database):
    os.makedirs(os.path.dirname(LORA_DB_PATH), exist_ok=True)
    # Write to a temp file first so a crash mid-write can't wipe the database.
    tmp_path = LORA_DB_PATH + ".tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(lora_database, f, indent=4, ensure_ascii=False)
    os.replace(tmp_path, LORA_DB_PATH)

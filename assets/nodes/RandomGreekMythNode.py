import requests
import random
import os
import json

class RandomGreekMythNode:
    """
    Fetches a random mythological figure.
    Caches data locally to avoid API Status 429 (Rate Limiting).
    """

    def __init__(self):
        # Determine the path for the cache files (same folder as the script)
        script_folder = os.path.dirname(os.path.realpath(__file__))
        self.cache_dir = os.path.join(script_folder, "..", "scripts")
        os.makedirs(self.cache_dir, exist_ok=True)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "category": (["gods", "heroes", "monsters", "titans"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("character_name", "description")
    FUNCTION = "get_myth"
    CATEGORY = "Creepybits/Text"

    def get_myth(self, category, seed):
        rng = random.Random(seed)
        cache_file = os.path.join(self.cache_dir, f"greek_{category}.json")

        data = None

        # 1. Try to load from local cache first
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                data = None # Force re-fetch if file is corrupt

        # 2. If no cache, fetch from API
        if not data:
            url = f"https://thegreekmythapi.vercel.app/api/{category}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # Save to cache immediately
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                elif response.status_code == 429:
                    return ("Error", "API Rate Limited (429). Try again in a few minutes or use existing cache.")
                else:
                    return ("Error", f"API Status {response.status_code}")
            except Exception as e:
                return ("Error", f"Connection Error: {str(e)}")

        # 3. Process the data (Local or freshly fetched)
        if isinstance(data, list) and len(data) > 0:
            choice = rng.choice(data)
            name = choice.get('name', 'Unknown')
            desc = choice.get('description', 'No description available.')

            attributes = choice.get('attributes', {})
            attr_str = ""
            if attributes:
                powers = attributes.get('powers', [])
                symbols = attributes.get('symbols', [])
                if powers:
                    attr_str += f" Powers: {', '.join(powers)}."
                if symbols:
                    attr_str += f" Symbols: {', '.join(symbols)}."

            return (name, f"{desc}{attr_str}")

        return ("Error", "No valid data found.")

# Node Registration
NODE_CLASS_MAPPINGS = {
    "RandomGreekMyth": RandomGreekMythNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomGreekMyth": "Random Greek Myth (Creepybits)"
}

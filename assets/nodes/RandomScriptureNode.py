import requests
import random

class RandomScriptureNode:
    """
    Fetches a random verse from the Bible, the Quran, or the Torah.
    Renamed for the 'Creepybits' Universal Archive.
    """

    # Chapter counts for the Five Books of Moses (Torah) for Sefaria randomization
    TORAH_MAP = {
        "Genesis": 50,
        "Exodus": 40,
        "Leviticus": 27,
        "Numbers": 36,
        "Deuteronomy": 34
    }

    # Your original Proverbs map
    PROVERBS_MAP = [
        33, 22, 35, 27, 23, 35, 27, 36, 18, 32, 31, 28, 25, 35, 33,
        33, 28, 24, 29, 30, 31, 29, 35, 34, 28, 28, 27, 28, 27, 33, 31
    ]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source": (["Bible (Whole)", "Bible (Proverbs Only)", "Quran", "Torah (Tanakh)"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("verse_text", "reference")
    FUNCTION = "get_scripture"
    CATEGORY = "Creepybits/Text"

    def get_scripture(self, source, seed):
        rng = random.Random(seed)

        # --- BIBLE LOGIC ---
        if source == "Bible (Whole)":
            url = "https://bible-api.com/?random=verse"
            return self._fetch_bible(url)

        elif source == "Bible (Proverbs Only)":
            chapter_idx = rng.randint(0, 30)
            chapter = chapter_idx + 1
            max_verse = self.PROVERBS_MAP[chapter_idx]
            verse = rng.randint(1, max_verse)
            url = f"https://bible-api.com/proverbs+{chapter}:{verse}"
            return self._fetch_bible(url)

        # --- QURAN LOGIC ---
        elif source == "Quran":
            # Using Pickthall translation for that 'Creepybits' archaic flavor
            url = "https://api.alquran.cloud/v1/ayah/random/en.pickthall"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()['data']
                    text = data['text'].strip()
                    ref = f"{data['surah']['englishName']} {data['surah']['number']}:{data['numberInSurah']}"
                    return (text, ref)
                return (f"Quran API Error: {response.status_code}", "Error")
            except Exception as e:
                return (f"Quran Connection Error: {str(e)}", "Error")

        # --- TORAH LOGIC (Sefaria) ---
        elif source == "Torah (Tanakh)":
            book = rng.choice(list(self.TORAH_MAP.keys()))
            max_chapters = self.TORAH_MAP[book]
            chapter = rng.randint(1, max_chapters)

            url = f"https://www.sefaria.org/api/texts/{book}.{chapter}?context=0"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    # Sefaria returns a list of verses for the chapter
                    verses = data.get('text', [])
                    if verses and isinstance(verses, list):
                        v_idx = rng.randint(0, len(verses) - 1)
                        text = verses[v_idx]
                        # Cleanup HTML tags Sefaria sometimes includes
                        import re
                        clean_text = re.sub('<[^<]+?>', '', text).strip()
                        ref = f"{book} {chapter}:{v_idx + 1}"
                        return (clean_text, ref)
                    return ("No text found in chapter", "Error")
                return (f"Sefaria API Error: {response.status_code}", "Error")
            except Exception as e:
                return (f"Sefaria Connection Error: {str(e)}", "Error")

        return ("Unknown Source", "Error")

    def _fetch_bible(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                clean_text = data.get('text', '').strip().replace('\n', ' ').replace('\r', '')
                return (clean_text, data.get('reference', 'Unknown'))
            return (f"Bible API Status {response.status_code}", "Error")
        except Exception as e:
            return (f"Bible Connection Error: {str(e)}", "Error")

# Node Registration
NODE_CLASS_MAPPINGS = {
    "RandomScripture": RandomScriptureNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomScripture": "Random Scripture (Creepybits)"
}

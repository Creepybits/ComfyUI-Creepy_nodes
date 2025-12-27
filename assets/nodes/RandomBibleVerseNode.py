import requests
import random

class RandomBibleVerseNode:
    """
    Fetches a random Bible verse from bible-api.com.
    Mode 'Random' gets any verse from the whole Bible.
    Mode 'Proverbs Only' ensures a wisdom quote from the book of Proverbs.
    """

    # Verse counts for all 31 chapters of Proverbs to ensure valid requests
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
                "mode": (["Random (Whole Bible)", "Proverbs Only (Wisdom)"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("verse_text", "reference")
    FUNCTION = "get_verse"
    CATEGORY = "Creepybits/Text"

    def get_verse(self, mode, seed):
        # We use the seed to initialize the random number generator
        # so that the same seed always produces the same 'random' choice locally
        rng = random.Random(seed)

        if mode == "Proverbs Only (Wisdom)":
            # 1. Pick a random chapter (1 to 31)
            chapter_idx = rng.randint(0, 30)
            chapter = chapter_idx + 1

            # 2. Pick a random verse valid for that chapter
            max_verse = self.PROVERBS_MAP[chapter_idx]
            verse = rng.randint(1, max_verse)

            # 3. Construct the direct URL
            url = f"https://bible-api.com/proverbs+{chapter}:{verse}"

        else:
            # Standard random verse from anywhere
            url = "https://bible-api.com/?random=verse"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                raw_text = data.get('text', '').strip()
                reference = data.get('reference', 'Unknown')

                # Cleanup text
                clean_text = raw_text.replace('\n', ' ').replace('\r', '')

                return (clean_text, reference)
            else:
                return (f"Error: API Status {response.status_code}", "Error")

        except Exception as e:
            return (f"Connection Error: {str(e)}", "Error")

# Node Registration
NODE_CLASS_MAPPINGS = {
    "RandomBibleVerse": RandomBibleVerseNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomBibleVerse": "Random Bible Verse (Creepybits)"
}

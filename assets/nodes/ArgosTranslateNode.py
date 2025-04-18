import argostranslate.package
import argostranslate.translate
import os
import json
import shutil  # Import the shutil module for file operations

class ArgosTranslateNode:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.dirname(self.script_dir) #Go up one directory level
        self.language_models_dir = os.path.join(self.assets_dir, "languages")
        self.available_languages = self.load_available_languages()

    def load_available_languages(self):
        language_models = {}
        for filename in os.listdir(self.language_models_dir):
            if filename.endswith(".argosmodel"):
                try:
                    from_code, to_code, version = self.extract_language_codes(filename)
                    language_models[(from_code, to_code)] = os.path.join(self.language_models_dir, filename)
                except ValueError:
                    print(f"Invalid filename format: {filename}")
        return language_models

    def extract_language_codes(self, filename):
        parts = filename.replace(".argosmodel", "").split("-")
        if len(parts) == 3 and parts[0] == "translate":
            from_code, to_code = parts[1].split("_")
            return from_code, to_code, parts[2]
        raise ValueError("Invalid filename format")

    @classmethod
    def INPUT_TYPES(cls):
        language_models = ArgosTranslateNode().available_languages
        available_languages = []
        for (from_code, to_code) in language_models:
            available_languages.append(f"{from_code} to {to_code}") # for the user

        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "translation_model": (available_languages,),  # All available languages
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "Creepybits/Translation"

    def translate(self, text, translation_model):
        from_code, to_code = translation_model.split(" to ") #Split to the "to" code
        try:
            translated_text = argostranslate.translate.translate(text, from_code, to_code)
            return (translated_text,)
        except Exception as e:
            print(f"Translation Error: {e}")
            return (f"Translation Error: {e}",)

    def download_model(self, from_lang, to_lang):
        try:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_lang and x.to_code == to_lang,
                    available_packages,
                ), None
            )

            if package_to_install:
                argostranslate.package.install_from_path(package_to_install.download())
                print(f"Downloaded and installed model for {from_lang} to {to_lang}")
            else:
                error_message = f"Error: No translation model found for {from_lang} to {to_lang}"
                print(error_message)
                return
        except Exception as e:
            print(f"Error in translation: {e}")

NODE_CLASS_MAPPINGS = {
    "ArgosTranslateNode": ArgosTranslateNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ArgosTranslateNode": "Argos Translate (Creepybits)",
}

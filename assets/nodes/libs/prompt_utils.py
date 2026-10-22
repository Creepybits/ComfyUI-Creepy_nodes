import os
import json

ASSETS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROMPTS_DIR = os.path.join(ASSETS_DIR, "prompts")


def prompt_path(filename):
    return os.path.join(PROMPTS_DIR, filename)


def prompt_mtime(filename):
    """Used by IS_CHANGED so editing a prompt file re-runs the node without restarting ComfyUI."""
    try:
        return os.path.getmtime(prompt_path(filename))
    except OSError:
        return 0.0


def read_prompt(filename):
    """Returns the prompt file's text, or an ERROR string (passed downstream) if it can't be read."""
    filepath = prompt_path(filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[Creepybits] Error: prompt file not found at {filepath}")
        return "ERROR: Prompt file not found."
    except Exception as e:
        print(f"[Creepybits] Error reading {filepath}: {e}")
        return f"ERROR: Could not read prompt file: {e}"


def load_prompt_list(json_file):
    """Reads the "prompts" list from a JSON file in assets/. Always returns a non-empty list,
    since ComfyUI can't build a dropdown from an empty one."""
    filepath = os.path.join(ASSETS_DIR, json_file)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            prompts = json.load(f).get("prompts", [])
    except FileNotFoundError:
        print(f"[Creepybits] Warning: {json_file} not found at {filepath}")
        prompts = []
    except Exception as e:
        print(f"[Creepybits] Warning: could not read {json_file}: {e}")
        prompts = []
    return prompts or [f"ERROR: No prompts listed in {json_file}"]


class FixedPromptNode:
    """Base for nodes that prepend a fixed prompt file to the user's text.
    Subclasses only set PROMPT_FILE."""
    PROMPT_FILE = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_2": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "concat_texts"
    CATEGORY = "Creepybits/Prompt"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return prompt_mtime(cls.PROMPT_FILE)

    def concat_texts(self, text_2):
        return (read_prompt(self.PROMPT_FILE) + text_2,)


class PromptListNode:
    """Base for nodes that output a prompt file picked from a JSON list.
    Subclasses only set PROMPT_LIST_FILE (and optionally CATEGORY)."""
    PROMPT_LIST_FILE = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_file": (load_prompt_list(cls.PROMPT_LIST_FILE),),
            },
            "optional": {
                "optional_input": ("*",)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "load_prompt"
    CATEGORY = "Creepybits/Prompt"

    @classmethod
    def IS_CHANGED(cls, prompt_file, **kwargs):
        return prompt_mtime(prompt_file)

    def load_prompt(self, prompt_file, optional_input=None):
        if prompt_file.startswith("ERROR:"):
            return (prompt_file,)
        return (read_prompt(prompt_file),)

import os
import json

from google import genai
from google.genai import types

# Default location of the API key config: assets/scripts/api_keys_config.json.
# Override with the CREEPYBITS_API_CONFIG environment variable if you keep it elsewhere.
DEFAULT_API_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts", "api_keys_config.json")
API_CONFIG_PATH = os.environ.get("CREEPYBITS_API_CONFIG", DEFAULT_API_CONFIG_PATH)

ENV_KEY_OPTION = "Environment (GEMINI_API_KEY)"
DEFAULT_THINKING_BUDGET = 4096

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-3-flash-preview",
]

SAFETY_THRESHOLD_MAP = {
    "Block None": "BLOCK_NONE",
    "Block Low": "BLOCK_LOW_AND_ABOVE",
    "Block Medium": "BLOCK_MEDIUM_AND_ABOVE",
    "Block High": "BLOCK_HIGH_AND_ABOVE",
}

HARM_CATEGORIES = [
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
]

_clients = {}


def _load_config():
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_api_key_list():
    keys = []
    if os.path.exists(API_CONFIG_PATH):
        try:
            keys = list(_load_config().keys())
        except Exception:
            keys = ["Error loading JSON"]
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or not keys:
        keys.append(ENV_KEY_OPTION)
    return keys


def resolve_api_key(selection):
    """Returns the API key for a dropdown selection. Key file paths in the config may be
    absolute or relative to the config file's folder."""
    if selection == ENV_KEY_OPTION:
        return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not os.path.exists(API_CONFIG_PATH):
        raise FileNotFoundError(f"API key config not found at {API_CONFIG_PATH}")

    key_file_path = _load_config().get(selection)
    if not key_file_path:
        return None
    if not os.path.isabs(key_file_path):
        key_file_path = os.path.join(os.path.dirname(API_CONFIG_PATH), key_file_path)
    if not os.path.exists(key_file_path):
        return None
    with open(key_file_path, "r", encoding="utf-8") as kf:
        return kf.read().strip() or None


def get_client(api_key):
    # Reuse clients so repeated runs don't pay the connection setup cost every time.
    client = _clients.get(api_key)
    if client is None:
        client = genai.Client(api_key=api_key)
        _clients[api_key] = client
    return client


def build_config(system_prompt, model, thinking_mode, safety_threshold, **params):
    config = {
        "system_instruction": system_prompt if system_prompt and system_prompt.strip() else None,
        "safety_settings": [
            types.SafetySetting(category=cat, threshold=SAFETY_THRESHOLD_MAP[safety_threshold])
            for cat in HARM_CATEGORIES
        ],
        **params,
    }

    # Gemini 2.5 Flash models think by default, and thinking tokens count against
    # max_output_tokens, which can leave nothing for the actual answer.
    if thinking_mode == "enable":
        config["thinking_config"] = types.ThinkingConfig(thinking_budget=DEFAULT_THINKING_BUDGET)
    elif "2.5-flash" in model:
        config["thinking_config"] = types.ThinkingConfig(thinking_budget=0)

    return types.GenerateContentConfig(**config)


def generate(api_key_selection, model, contents, config):
    try:
        api_key = resolve_api_key(api_key_selection)
    except Exception as e:
        return f"Error reading key config: {e}"
    if not api_key:
        return "Error: API key not found."

    try:
        client = get_client(api_key)
    except Exception as e:
        return f"Error initializing Client: {e}"

    try:
        response = client.models.generate_content(model=model, contents=contents, config=config)
    except Exception as e:
        return f"API Error: {str(e)}"

    if response.text:
        return response.text

    # No text usually means the prompt or the answer was blocked, or the token limit was hit.
    reason = None
    if response.prompt_feedback and response.prompt_feedback.block_reason:
        reason = f"prompt blocked ({response.prompt_feedback.block_reason})"
    elif response.candidates and response.candidates[0].finish_reason:
        reason = f"finish reason {response.candidates[0].finish_reason}"
    return f"Error: Gemini returned no text ({reason or 'unknown reason'})."

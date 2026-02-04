import os
import json
import base64
from google import genai
from google.genai import types
from io import BytesIO
from PIL import Image
import torch
import torchaudio
import numpy as np

# Path to your central API key config
API_CONFIG_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\api_keys_config.json"
DEFAULT_THINKING_BUDGET = 4096

SAFETY_THRESHOLD_MAP = {
    "Block None": "BLOCK_NONE",
    "Block Low": "BLOCK_LOW_AND_ABOVE",
    "Block Medium": "BLOCK_MEDIUM_AND_ABOVE",
    "Block High": "BLOCK_HIGH_AND_ABOVE",
}

def get_api_key_list():
    if os.path.exists(API_CONFIG_PATH):
        try:
            with open(API_CONFIG_PATH, 'r') as f:
                config = json.load(f)
                return list(config.keys())
        except Exception:
            return ["Error loading JSON"]
    return ["Config not found"]

class GeminiAudioAnalyzer:
    """
    Updated for google-genai SDK (Jan 2026).
    Includes the 'Handshake Fix' for empty audio/instruction inputs.
    """

    CATEGORY = "Creepybits/Audio"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    @classmethod
    def INPUT_TYPES(s):
        key_list = get_api_key_list()
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a professional audio analyst."}),
                "user_instructions": ("STRING", {"multiline": True, "default": "Describe the audio input in detail."}),
                "model": (["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-flash-lite-preview-09-2025", "gemini-2.5-flash-preview-09-2025", "gemini-2.0-flash-exp"],),
                "api_key_selection": (key_list,),
            },
            "optional": {
                "audio": ("AUDIO", ),
                "max_output_tokens": ("INT", {"default": 2048, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.1}),
                "thinking_mode": (["disable", "enable"], {"default": "disable"}),
                "safety_threshold": (list(SAFETY_THRESHOLD_MAP.keys()), {"default": "Block None"}),
            }
        }

    def generate_content(self, system_prompt, user_instructions, model, api_key_selection,
                         audio=None, max_output_tokens=2048, temperature=0.4,
                         thinking_mode="disable", safety_threshold="Block None"):

        # --- API Key Extraction ---
        api_key = None
        if os.path.exists(API_CONFIG_PATH):
            try:
                with open(API_CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                    key_file_path = config.get(api_key_selection)
                    if key_file_path and os.path.exists(key_file_path):
                        with open(key_file_path, 'r') as kf:
                            api_key = kf.read().strip()
            except Exception as e:
                return (f"Error reading key config: {e}",)

        if not api_key: return ("Error: Gemini API key not found.",)

        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            return (f"Error initializing Client: {e}",)

        # Prepare Content Parts
        contents = []
        if user_instructions and user_instructions.strip():
            contents.append(user_instructions.strip())

        # Process Audio if present
        if audio is not None:
            try:
                waveform = audio["waveform"]
                sample_rate = audio["sample_rate"]
                if waveform.dim() == 3: waveform = waveform.squeeze(0)
                elif waveform.dim() == 1: waveform = waveform.unsqueeze(0)
                if waveform.shape[0] > 1: waveform = torch.mean(waveform, dim=0, keepdim=True)
                if sample_rate != 16000: waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
                buffer = BytesIO()
                torchaudio.save(buffer, waveform, 16000, format="WAV")
                contents.append(types.Part.from_bytes(data=buffer.getvalue(), mime_type="audio/wav"))
            except Exception as e:
                return (f"Error processing audio: {e}",)

        # --- THE FIX: Fallback for No-Audio / No-Instruction Mode ---
        if not contents:
            if system_prompt and system_prompt.strip():
                # Satisfy the requirement for at least one User message
                contents.append("Please provide an analysis based on your current instructions.")
            else:
                return ("Error: No input provided (need system prompt, instructions, or audio).",)

        # Build Config
        safety_settings = [
            types.SafetySetting(category=cat, threshold=SAFETY_THRESHOLD_MAP[safety_threshold])
            for cat in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
                        "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
        ]

        generate_config = {
            "system_instruction": system_prompt if system_prompt.strip() else None,
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "safety_settings": safety_settings,
        }

        if thinking_mode == "enable":
            generate_config["thinking_config"] = {"include_thoughts": True}

        # API Call
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(**generate_config)
            )
            return (response.text,)
        except Exception as e:
            return (f"API Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {"GeminiAudioAnalyzer": GeminiAudioAnalyzer}
NODE_DISPLAY_NAME_MAPPINGS = {"GeminiAudioAnalyzer": "Gemini Audio Analyzer Unified (Creepybits)"}

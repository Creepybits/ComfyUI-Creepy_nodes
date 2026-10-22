import io
import wave

import numpy as np
import torch
import torchaudio
from google.genai import types

from .libs.gemini_common import GEMINI_MODELS, SAFETY_THRESHOLD_MAP, get_api_key_list, build_config, generate


def waveform_to_wav_bytes(waveform, sample_rate):
    """Encodes a mono float waveform as 16-bit PCM WAV. Done with the stdlib so it doesn't
    depend on whichever audio backend torchaudio happens to have installed."""
    pcm = (waveform.clamp(-1.0, 1.0).squeeze(0).cpu().numpy() * 32767).astype(np.int16)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())
    return buffer.getvalue()


class GeminiAudioAnalyzer:
    CATEGORY = "Creepybits/Audio"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a professional audio analyst."}),
                "user_instructions": ("STRING", {"multiline": True, "default": "Describe the audio input in detail."}),
                "model": (GEMINI_MODELS,),
                "api_key_selection": (get_api_key_list(),),
            },
            "optional": {
                "audio": ("AUDIO", ),
                "max_output_tokens": ("INT", {"default": 2048, "min": 1, "max": 65536}),
                "temperature": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 2.0, "step": 0.1}),
                "thinking_mode": (["disable", "enable"], {"default": "disable"}),
                "safety_threshold": (list(SAFETY_THRESHOLD_MAP.keys()), {"default": "Block None"}),
                "custom_model": ("STRING", {"default": "", "tooltip": "Overrides the model dropdown, e.g. for newly released Gemini models."}),
            }
        }

    def generate_content(self, system_prompt, user_instructions, model, api_key_selection,
                         audio=None, max_output_tokens=2048, temperature=0.4,
                         thinking_mode="disable", safety_threshold="Block None", custom_model=""):
        model = custom_model.strip() or model

        contents = []
        if user_instructions and user_instructions.strip():
            contents.append(user_instructions.strip())

        if audio is not None:
            try:
                waveform = audio["waveform"]
                sample_rate = audio["sample_rate"]
                if waveform.dim() == 3:
                    waveform = waveform[0]
                elif waveform.dim() == 1:
                    waveform = waveform.unsqueeze(0)
                if waveform.shape[0] > 1:
                    waveform = torch.mean(waveform, dim=0, keepdim=True)
                if sample_rate != 16000:
                    waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
                contents.append(types.Part.from_bytes(data=waveform_to_wav_bytes(waveform, 16000), mime_type="audio/wav"))
            except Exception as e:
                return (f"Error processing audio: {e}",)

        # Gemini needs at least one user message, even when everything is in the system prompt.
        if not contents:
            if system_prompt and system_prompt.strip():
                contents.append("Please provide an analysis based on your current instructions.")
            else:
                return ("Error: No input provided (need system prompt, instructions, or audio).",)

        config = build_config(system_prompt, model, thinking_mode, safety_threshold,
                              temperature=temperature, max_output_tokens=max_output_tokens)
        return (generate(api_key_selection, model, contents, config),)


NODE_CLASS_MAPPINGS = {"GeminiAudioAnalyzer": GeminiAudioAnalyzer}
NODE_DISPLAY_NAME_MAPPINGS = {"GeminiAudioAnalyzer": "Gemini Audio Analyzer Unified (Creepybits)"}

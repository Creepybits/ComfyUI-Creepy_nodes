import os
import json
import base64
import requests
import google.generativeai as genai
from io import BytesIO
from PIL import Image
import torch
import torchaudio
import numpy as np

DEFAULT_API_KEY_PATH = r"C:\AI\Comfy\ComfyUI\custom_nodes\Creepy_nodes\assets\scripts\gemini_api_key.txt"

SAFETY_THRESHOLDS = ["Block None", "Block Low", "Block Medium", "Block High"]

SAFETY_THRESHOLD_MAP = {
    "Block None": "BLOCK_NONE",
    "Block Low": "BLOCK_LOW_AND_ABOVE",
    "Block Medium": "BLOCK_MEDIUM_AND_ABOVE",
    "Block High": "BLOCK_HIGH_AND_ABOVE",
}

SAFETY_CATEGORIES = [
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
]


class GeminiAudioAnalyzer:
    """
    A custom node for ComfyUI that uses the Google Gemini API for text generation
    with audio analysis capabilities.
    Loads API key from input field or default file.
    """

    CATEGORY = "Creepybits/Audio"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("generated_content",)
    FUNCTION = "generate_content"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Analyze the audio input.", "multiline": True}),
                "input_type": (["text", "audio"], {"default": "text"}),
                "model_version": (["gemini-2.5-flash-preview-05-20", "gemini-2.0-flash", "gemini-2.5-flash-lite-preview-06-17", "gemini-2.0-flash-lite"], {"default": "gemini-2.0-flash"}),
                "operation_mode": (["analysis", "generate_images"], {"default": "analysis"}),
            },
            "optional": {
                "Additional_Context": ("STRING", {"default": "", "multiline": True}),
                "audio": ("AUDIO", ),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "max_output_tokens": ("INT", {"default": 2048, "min": 1, "max": 8192}),
                "temperature": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.1}),
                "safety_threshold": (SAFETY_THRESHOLDS, {"default": "Block None"}),
            }
        }

    def __init__(self):
        self.chat_history = []

    def load_api_key(self, api_key=""):
        """
        Loads the API key from the provided string parameter or the default file.
        Prioritizes the provided string.
        """
        if api_key and api_key.strip():
            return api_key.strip()

        try:
            with open(DEFAULT_API_KEY_PATH, "r") as f:
                file_content = f.read()
                stripped_key = file_content.strip()

                if stripped_key:
                     return stripped_key
                else:
                     print(f"Warning: API key file at '{DEFAULT_API_KEY_PATH}' is empty or contains only whitespace.")
                     return None

        except FileNotFoundError:
            print(f"Warning: API key file not found at {DEFAULT_API_KEY_PATH}. Tried to load because node input was empty.")
            return None
        except Exception as e:
            print(f"Warning: Error reading API key file: {e}")
            return None


    def prepare_content(self, prompt, input_type, Additional_Context=None, audio=None):
        """Prepares the content for the Gemini API based on the input type."""
        text_content = prompt if not Additional_Context else f"{prompt}\n\n{Additional_Context.strip()}"

        if input_type == "text":
            return [text_content]

        elif input_type == "audio" and audio is not None:
            content_parts = []
            if text_content.strip():
                 content_parts.append({"text": text_content.strip()})

            try:
                waveform = audio["waveform"]
                sample_rate = audio["sample_rate"]

                if waveform.dim() == 3:
                    waveform = waveform.squeeze(0)
                elif waveform.dim() == 1:
                    waveform = waveform.unsqueeze(0)

                if waveform.shape[0] > 1:
                    waveform = torch.mean(waveform, dim=0, keepdim=True)

                if sample_rate != 16000:
                    waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)

                buffer = BytesIO()
                torchaudio.save(buffer, waveform, 16000, format="WAV")
                audio_bytes = buffer.getvalue()

                content_parts.append({
                    "inline_data": {
                        "mime_type": "audio/wav",
                        "data": base64.b64encode(audio_bytes).decode('utf-8')
                    }
                })

            except KeyError as e:
                 raise ValueError(f"Invalid audio input format: Missing key {e}") from e
            except Exception as e:
                 raise ValueError(f"Failed to process audio input: {e}") from e

            return content_parts

        else:
            if input_type == "audio" and audio is None:
                 raise ValueError("Input type set to 'audio', but no audio input was provided.")
            else:
                 raise ValueError(f"Invalid input_type: '{input_type}'. Must be 'text' or 'audio'.")


    def generate_content(self, prompt, input_type, model_version="gemini-2.0-flash",
                        operation_mode="analysis", Additional_Context=None,
                        audio=None, api_key="", max_output_tokens=8192,
                        safety_threshold="Block None", temperature=0.4):
        """Generate content using Gemini model with various input types (text, audio)."""

        # --- API Key Loading ---
        resolved_api_key = self.load_api_key(api_key)

        if not resolved_api_key or not resolved_api_key.strip():
            return ("Error: Gemini API key not found or loaded for Audio Analyzer. Please provide key in node input, set GOOGLE_API_KEY env var, or ensure valid key in default file. Check console output for details.",)

        # --- Configure Gemini Library ---
        try:
            genai.configure(api_key=resolved_api_key)
            print("[AudioAnalyzer] Gemini API Key configured successfully.")

        except Exception as e:
             error_message_detail = str(e)
             if hasattr(e, 'response') and e.response:
                  if hasattr(e.response, 'text'):
                       try:
                            error_json = json.loads(e.response.text)
                            if 'error' in error_json and 'message' in error_json['error']:
                                 api_error_message = error_json['error']['message']
                                 error_message_detail = f"API Error during configuration: {api_error_message}"
                       except (json.JSONDecodeError, AttributeError):
                            pass

             print(f"[AudioAnalyzer] Error configuring Gemini API: {error_message_detail}")
             return (f"Error configuring Gemini API: {error_message_detail}",)


        # --- Configure Safety Settings ---
        safety_settings = []
        api_threshold = SAFETY_THRESHOLD_MAP.get(safety_threshold, "BLOCK_NONE")

        if api_threshold != "BLOCK_NONE":
            for category_name in SAFETY_CATEGORIES:
                safety_settings.append({
                    "category": category_name,
                    "threshold": api_threshold
                })

        # --- Configure Generation Parameters ---
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )

        # --- Get the Generative Model Instance ---
        try:
            model = genai.GenerativeModel(
                model_name=model_version,
                safety_settings=safety_settings,
                generation_config=generation_config
            )
            print(f"[AudioAnalyzer] Model instance created for '{model_version}'.")

        except Exception as e:
            if "Invalid model" in str(e):
                 return (f"Error: Invalid model name '{model_version}'. Check model availability.",)
            return (f"Error: Could not get Gemini model '{model_version}'. Check model name, API status, or internet connection: {e}",)


        # --- Prepare Content (Text + Optional Audio) ---
        try:
            content_parts = self.prepare_content(prompt, input_type, Additional_Context, audio)
        except ValueError as e:
             return (f"Error preparing content: {e}",)
        except Exception as e:
             return (f"Unexpected error preparing content: {e}",)


        # --- Send API Request ---
        try:
            print("[AudioAnalyzer] Sending generate_content request...")
            response = model.generate_content(
                contents=content_parts,
            )
            print("[AudioAnalyzer] API request finished.")


            # --- Process Response ---
            generated_content = ""
            if hasattr(response, 'text'):
                 generated_content = response.text

            if not generated_content:
                 print("[AudioAnalyzer] Generated text is empty or extraction failed.")

                 if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                     feedback_info = {}
                     if hasattr(response.prompt_feedback, 'block_reason') and response.prompt_feedback.block_reason and hasattr(response.prompt_feedback.block_reason, 'name') and response.prompt_feedback.block_reason.name != 'UNASSIGNED':
                          print(f"  Block Reason: {response.prompt_feedback.block_reason.name}")
                          feedback_info['block_reason'] = response.prompt_feedback.block_reason.name

                     if hasattr(response.prompt_feedback, 'safety_ratings') and response.prompt_feedback.safety_ratings:
                         print("  Safety Ratings:")
                         feedback_info['safety_ratings'] = []
                         for rating in response.prompt_feedback.safety_ratings:
                             if hasattr(rating, 'probability') and hasattr(rating.probability, 'name') and rating.probability.name != 'UNSPECIFIED':
                                 rating_info = {"category": rating.category.name, "probability": rating.probability.name}
                                 print(f"    Category: {rating_info['category']}, Probability: {rating_info['probability']}")
                                 feedback_info['safety_ratings'].append(rating_info)

                     if 'block_reason' in feedback_info:
                          return (f"Error: Content generation blocked due to {feedback_info['block_reason']}. Check console for safety feedback.",)
                     elif 'safety_ratings' in feedback_info and feedback_info['safety_ratings']:
                          return ("Error: No text generated. High safety ratings. Check console for details.",)
                     return ("Error: No text generated. API returned empty content/candidates. Check Prompt Feedback in console.",)
                 else:
                      if hasattr(response, 'candidates') and not response.candidates:
                           return ("Error: API returned no candidates (likely blocked). No prompt feedback details available.",)
                      return ("Error: No text generated from the API and no specific feedback provided. Check console.",)


            return (generated_content,)

        except Exception as e:
            print(f"[AudioAnalyzer] An error occurred during Gemini API call: {e}")

            error_message_detail = str(e)
            if hasattr(e, 'response') and e.response:
                 if hasattr(e.response, 'text'):
                      try:
                           error_json = json.loads(e.response.text)
                           if 'error' in error_json and 'message' in error_json['error']:
                                api_error_message = error_json['error']['message']
                                error_message_detail = f"API Error: {api_error_message}"
                           elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                error_message_detail = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                      except (json.JSONDecodeError, AttributeError):
                           if hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                                error_message_detail = f"HTTP Error: {e.response.status_code} {e.response.reason}"
                           pass

                 elif hasattr(e.response, 'status_code') and hasattr(e.response, 'reason'):
                      error_message_detail = f"HTTP Error: {e.response.status_code} {e.response.reason}"

            return (f"Error: An error occurred during Gemini API call: {error_message_detail}",)


NODE_CLASS_MAPPINGS = {
    "GeminiAudioAnalyzer": GeminiAudioAnalyzer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiAudioAnalyzer": "Gemini Audio Analyzer (Creepybits)",
}
import torch
import torchaudio
import random
import math

class RandomAudioSegment:
    CATEGORY = "Creepybits/Audio"
    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "get_random_segment"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "segment_length": ("FLOAT", {
                    "default": 10.0,
                    "min": 0.1,
                    "max": 600.0,
                    "step": 0.1,
                    "display": "number"
                }),
            },
            "optional": {
                "start_time": ("FLOAT", {
                    "default": -1.0,
                    "min": -1.0,
                    "step": 0.1,
                    "display": "number"
                }),
            }
        }

    def get_random_segment(self, audio, segment_length=10.0, start_time=-1.0):
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        if segment_length <= 0:
             segment_length = 10.0
        if math.isnan(segment_length):
             segment_length = 10.0

        total_duration = waveform.shape[-1] / sample_rate
        actual_segment_length = min(segment_length, total_duration)
        max_possible_start_time = total_duration - actual_segment_length

        selected_start_time = 0.0

        if start_time >= 0.0 and not math.isnan(start_time):
            selected_start_time = start_time

            if max_possible_start_time > 0 and selected_start_time > max_possible_start_time:
                selected_start_time = max_possible_start_time
            elif max_possible_start_time <= 0 and selected_start_time > 0:
                 selected_start_time = 0.0
        else:
            if max_possible_start_time <= 0:
                selected_start_time = 0.0
                actual_segment_length = total_duration
            else:
                selected_start_time = random.uniform(0.0, max_possible_start_time)

        start_sample = int(selected_start_time * sample_rate)
        num_samples = int(actual_segment_length * sample_rate)
        end_sample = start_sample + num_samples

        end_sample = min(end_sample, waveform.shape[-1])
        actual_num_samples_extracted = end_sample - start_sample

        if actual_num_samples_extracted <= 0:
             segment = torch.empty(*waveform.shape[:-1], 0, dtype=waveform.dtype, device=waveform.device)
             extracted_duration = 0.0
        else:
             segment = waveform[..., start_sample:end_sample]
             extracted_duration = actual_num_samples_extracted / sample_rate

        new_audio = {
            "waveform": segment,
            "sample_rate": sample_rate,
        }

        return (new_audio,)


NODE_CLASS_MAPPINGS = {
    "RandomAudioSegment": RandomAudioSegment,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomAudioSegment": "Random/Fixed Audio Picker (Creepybits)",
}

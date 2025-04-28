# --- START OF FILE RandomAudioSegment.py ---

import torch
import torchaudio
import random
import math # Import math for isnan

class RandomAudioSegment:
    CATEGORY = "Creepybits/Audio"  # Or your preferred category
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
                    "min": 0.1,     # Minimum segment length
                    "max": 600.0,   # Maximum segment length (e.g., 10 minutes)
                    "step": 0.1,
                    "display": "number" # Explicitly hint as a number input
                }),
            },
            "optional": {
                # Add the new input for fixed start time
                # Use -1.0 as a sentinel value to indicate "use random start time"
                "start_time": ("FLOAT", {
                    "default": -1.0, # Default to -1.0 to trigger random selection
                    "min": -1.0,    # Allow -1.0 (or any negative) for random, 0.0 or positive for fixed
                    "step": 0.1,
                    "display": "number"
                }),
            }
        }

    # Update the function signature to accept the new parameter
    def get_random_segment(self, audio, segment_length=10.0, start_time=-1.0): # Add start_time with default -1.0
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        # Ensure segment_length is positive
        if segment_length <= 0:
             print(f"[RandomAudioSegment] Warning: segment_length must be positive ({segment_length} provided). Using default 10.0.")
             segment_length = 10.0
        # Handle potential NaN from UI
        if math.isnan(segment_length):
             print(f"[RandomAudioSegment] Warning: segment_length is NaN. Using default 10.0.")
             segment_length = 10.0


        # Calculate total duration in seconds
        total_duration = waveform.shape[-1] / sample_rate

        # Determine the actual segment length to extract (capped by total duration)
        actual_segment_length = min(segment_length, total_duration)

        # Calculate maximum possible start time for this actual segment length
        max_possible_start_time = total_duration - actual_segment_length

        selected_start_time = 0.0 # Initialize selected start time in seconds

        # Check if a fixed start time is provided (start_time >= 0)
        if start_time >= 0.0 and not math.isnan(start_time): # Also check for NaN
            print(f"[RandomAudioSegment] Fixed start time provided: {start_time:.2f}s")
            selected_start_time = start_time

            # Clamp the requested start time to the valid range if necessary
            if max_possible_start_time > 0 and selected_start_time > max_possible_start_time:
                print(f"[RandomAudioSegment] Warning: Requested start time {start_time:.2f}s exceeds maximum possible start time {max_possible_start_time:.2f}s for segment length {actual_segment_length:.2f}s. Clamping start time.")
                selected_start_time = max_possible_start_time
            elif max_possible_start_time <= 0 and selected_start_time > 0:
                 # Handle case where audio is shorter than segment, but user gave positive start time
                 print(f"[RandomAudioSegment] Warning: Audio ({total_duration:.2f}s) is shorter than or equal to segment length ({actual_segment_length:.2f}s). Fixed start time > 0 is invalid. Starting at 0.")
                 selected_start_time = 0.0


        else:
            # If start_time is negative or NaN, use random start time logic
            print(f"[RandomAudioSegment] Using random start time (start_time input was {start_time}).")
            if max_possible_start_time <= 0:
                # If audio is shorter than or equal to the desired segment length, start at 0
                selected_start_time = 0.0
                # The actual segment length will be the total duration in this case
                actual_segment_length = total_duration
                print(f"[RandomAudioSegment] Audio too short for requested segment length. Using full audio from start: 0.0s, length: {actual_segment_length:.2f}s.")
            else:
                # Otherwise, select a random start time within the valid range
                selected_start_time = random.uniform(0.0, max_possible_start_time)
                print(f"[RandomAudioSegment] Random start time selected: {selected_start_time:.2f}s, length: {actual_segment_length:.2f}s.")

        # Convert start time to number of samples
        start_sample = int(selected_start_time * sample_rate)

        # Calculate end sample based on start_sample and actual_segment_length
        num_samples = int(actual_segment_length * sample_rate)
        end_sample = start_sample + num_samples

        # Handle potential off-by-one or floating point issues at the end
        # Ensure end_sample does not exceed the total number of samples in the original waveform
        end_sample = min(end_sample, waveform.shape[-1])

        # Recalculate actual number of samples extracted based on the clamped end_sample
        actual_num_samples_extracted = end_sample - start_sample

        # Basic check: if actual_num_samples_extracted ended up 0 or negative, return an empty segment
        if actual_num_samples_extracted <= 0:
             print(f"[RandomAudioSegment] Warning: Calculated segment resulted in zero or less samples. Returning empty audio.")
             # Return an empty tensor with the correct shape (channels, 0) or (batch, channels, 0)
             # Need to preserve leading dimensions (batch, channels)
             segment = torch.empty(*waveform.shape[:-1], 0, dtype=waveform.dtype, device=waveform.device)
             extracted_duration = 0.0 # Duration is zero for empty segment
        else:
             # Extract segment using calculated samples
             # Assuming waveform is [batch, channels, samples] or [channels, samples]
             # Use slicing on the last dimension (samples)
             segment = waveform[..., start_sample:end_sample]
             extracted_duration = actual_num_samples_extracted / sample_rate # Calculate actual duration extracted


        print(f"[RandomAudioSegment] Extracted segment: Start Sample={start_sample}, End Sample={end_sample}, Actual Samples={actual_num_samples_extracted}, Duration={extracted_duration:.2f}s")


        # Create new audio dictionary
        new_audio = {
            "waveform": segment,
            "sample_rate": sample_rate,
        }

        return (new_audio,) # Return as a tuple


NODE_CLASS_MAPPINGS = {
    "RandomAudioSegment": RandomAudioSegment,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomAudioSegment": "Random/Fixed Audio Picker (Creepybits)", # Updated display name
}

# --- END OF FILE RandomAudioSegment.py ---

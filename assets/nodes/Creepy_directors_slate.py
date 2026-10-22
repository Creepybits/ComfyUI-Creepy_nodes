# creepy_directors_slate.py
from .libs.prompt_utils import read_prompt, prompt_mtime


class CreepyDirectorsSlate:
    """
    A user-friendly node to generate and enhance prompts for cinematic video generation.
    V5.0 - The Artist's Edition. Uses a library of high-level, conceptually-driven,
    named cinematic shots with intensity modifiers, based on proven R&D.
    """
    PROMPT_FILE = "CINEMATOGRAPHER.txt"

    # The definitive, battle-tested library of narrative cinematic motion prompts.
    MOTION_PRESETS = {
        "Static": {
            "No Movement": "A still, static, unmoving shot. No camera movement."
        },
        "Dolly Zoom (Vertigo)": {
            "Slow": "A slow dolly zoom (Vertigo effect), the subject stays the same size while the background compresses.",
            "Medium": "A medium dolly zoom (Vertigo effect).",
            "Strong": "A dramatic dolly zoom (Vertigo effect), the background warps and compresses rapidly."
        },
        "Tracking Shot (Follow)": {
            "Slow": "A cinematic slow tracking shot, following the subject.",
            "Medium": "A cinematic tracking shot, following the subject.",
            "Strong": "A fast-paced tracking shot, closely following the subject's every move."
        },
        "Pan": {
            "Slow Left": "A cinematic slow pan from right to left.",
            "Medium Left": "A cinematic pan from right to left.",
            "Slow Right": "A cinematic slow pan from left to right.",
            "Medium Right": "A cinematic pan from left to right."
        },
        "Tilt": {
            "Slow Up": "A cinematic slow tilt from bottom to top.",
            "Medium Up": "A cinematic tilt from bottom to top.",
            "Slow Down": "A cinematic slow tilt from top to bottom.",
            "Medium Down": "A cinematic tilt from top to bottom."
        },
        "Roll (Dutch Angle)": {
            "Slow Clockwise": "The camera slowly rolls, tilting the horizon clockwise for a disorienting Dutch angle effect.",
            "Slow Anticlockwise": "The camera slowly rolls, tilting the horizon anticlockwise for a disorienting Dutch angle effect."
        },
        "Crane Shot": {
            "Rise Up": "A sweeping crane shot, starting low and rising high to reveal the scene.",
            "Descend Down": "A sweeping crane shot, starting high and descending down to focus on the subject."
        }
    }

    # We flatten the nested dictionary into a single list for the dropdown
    FLAT_PRESETS = []
    for motion, intensities in MOTION_PRESETS.items():
        for intensity, schedule in intensities.items():
            FLAT_PRESETS.append(f"{motion}: {intensity}")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive_prompt": ("STRING", {"multiline": True, "default": "masterpiece, cinematic, 4k"}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "blurry, low quality, cartoon"}),
                "motion_preset": (s.FLAT_PRESETS,),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("positive_prompt_out", "negative_prompt_out",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Creepybits"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return prompt_mtime(cls.PROMPT_FILE)

    def generate_prompt(self, positive_prompt, negative_prompt, motion_preset):

        # Parse the combined preset string to find the motion and intensity
        motion_type, intensity = motion_preset.split(": ", 1)

        # Get the correct camera schedule from our nested dictionary
        camera_schedule = self.MOTION_PRESETS[motion_type][intensity]

        # Append the conceptual camera command to the positive prompt
        if camera_schedule:
            # We add a period and space for natural language separation
            final_positive_prompt = f"{read_prompt(self.PROMPT_FILE)}. {positive_prompt}. {camera_schedule}"
        else:
            final_positive_prompt = positive_prompt

        return (final_positive_prompt, negative_prompt)

# Add the node to ComfyUI's node list
NODE_CLASS_MAPPINGS = {
    "CreepyDirector'sSlate": CreepyDirectorsSlate
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CreepyDirector'sSlate": "Director's Slate"
}

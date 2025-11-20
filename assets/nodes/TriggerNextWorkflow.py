import requests
import json
import os

class TriggerNextWorkflow:
    def __init__(self):
        pass

    # This is what creates the input slot in ComfyUI
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # Creates a text widget for the path
                "json_path": ("STRING", {"default": "C:\\path\\to\\workflow_B.json", "multiline": False}),
                # Just a dummy input to force execution order (connect your Image Save node here)
                "trigger_image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "execute_next"
    CATEGORY = "Creepybits/MadScience"

    def execute_next(self, json_path, trigger_image):
        # Verify the file exists first
        if not os.path.exists(json_path):
            return (f"Error: File not found at {json_path}",)

        # Load the workflow file
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except Exception as e:
            return (f"Error loading JSON: {str(e)}",)

        # The Payload: ComfyUI API expects the workflow in a 'prompt' key
        payload = {"prompt": workflow_data}

        # Send to local API
        try:
            # Note: 8188 is default, you might need to change if you use a different port
            response = requests.post("http://127.0.0.1:8188/prompt", json=payload)

            if response.status_code == 200:
                return ("Successfully queued next workflow!",)
            else:
                return (f"Failed to queue. Status: {response.status_code}",)

        except Exception as e:
            return (f"API Connection Failed: {str(e)}",)

# Node Mappings
NODE_CLASS_MAPPINGS = {
    "TriggerNextWorkflow": TriggerNextWorkflow
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TriggerNextWorkflow": "Chain Workflow (API)"
}

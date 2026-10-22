import requests
import json
import os


def local_prompt_url():
    """URL of this ComfyUI's /prompt endpoint, so a custom --port or --listen keeps working."""
    try:
        from server import PromptServer
        server = PromptServer.instance
        address = server.address if server.address not in (None, "", "0.0.0.0", "::") else "127.0.0.1"
        if ":" in address:
            address = f"[{address}]"
        return f"http://{address}:{server.port}/prompt"
    except Exception:
        return "http://127.0.0.1:8188/prompt"

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

        # Workflows saved with the normal "Save" have a "nodes" list; the API needs "Export (API)" format.
        if isinstance(workflow_data, dict) and "nodes" in workflow_data:
            return ("Error: This is a UI workflow file. Save it with 'Export (API)' and point to that file instead.",)

        # The Payload: ComfyUI API expects the workflow in a 'prompt' key
        payload = {"prompt": workflow_data}

        # Send to local API
        try:
            response = requests.post(local_prompt_url(), json=payload, timeout=30)

            if response.status_code == 200:
                return ("Successfully queued next workflow!",)
            else:
                return (f"Failed to queue. Status: {response.status_code} {response.text[:500]}",)

        except Exception as e:
            return (f"API Connection Failed: {str(e)}",)

# Node Mappings
NODE_CLASS_MAPPINGS = {
    "TriggerNextWorkflow": TriggerNextWorkflow
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TriggerNextWorkflow": "Chain Workflow (API)"
}

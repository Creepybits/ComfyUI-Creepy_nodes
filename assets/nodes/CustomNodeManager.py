import os
import ast
import json


class CustomNodeManager:
    def __init__(self):
        self.custom_nodes_dir = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "scan_mode": (["Validate Python", "Check Libraries"],),
                "directory": ("STRING", {"default": ""}),
                              "scan": ("BOOLEAN", {"default": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("node_info",)
    FUNCTION = "get_node_info"
    CATEGORY = "Creepybits/Utilities"

    def get_node_info(self, scan_mode, directory, scan):
        directory_to_scan = directory or self.custom_nodes_dir

        node_info = {}

        for filename in sorted(os.listdir(directory_to_scan)):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    # Files are parsed, not imported: importing ran every file's top-level code
                    # (and re-imported its dependencies) just to inspect it.
                    filepath = os.path.join(directory_to_scan, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=filepath)

                    if scan_mode == "Validate Python":
                        assigned = {
                            target.id
                            for node in tree.body if isinstance(node, (ast.Assign, ast.AnnAssign))
                            for target in (node.targets if isinstance(node, ast.Assign) else [node.target])
                            if isinstance(target, ast.Name)
                        }
                        if "NODE_CLASS_MAPPINGS" in assigned:
                            node_info[filename] = f"Name {filename} is valid!"
                        else:
                            node_info[filename] = f"Name {filename} invalid. Missing attribute mappings"

                    elif scan_mode == "Check Libraries":
                        imported_modules = []
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.Import, ast.ImportFrom)):
                                imported_modules.extend(alias.name for alias in node.names)
                        if imported_modules:
                            node_info[filename] = f"File {filename} imports {imported_modules}"

                except Exception as e:
                    node_info[filename] = f"Error processing {filename}: {e}"

        output_string = json.dumps(node_info, indent=4)

        return (output_string,)

NODE_CLASS_MAPPINGS = {
    "CustomNodeManager": CustomNodeManager
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomNodeManager": "Custom Node Manager (Creepybits)"
}

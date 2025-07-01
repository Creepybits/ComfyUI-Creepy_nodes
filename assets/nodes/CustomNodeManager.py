import os
import ast
import importlib.util
import sys
import json
import inspect #Needed
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
        if directory:
            directory_to_scan = directory
        else:
            directory_to_scan =  self.custom_nodes_dir

        node_info = {}       

        for filename in os.listdir(directory_to_scan):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    filepath = os.path.join(directory_to_scan, filename)                    
                    module_name = os.path.splitext(filename)[0]
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    valid = False

                    if scan_mode == "Validate Python":
                        valid_py = hasattr(module, "NODE_CLASS_MAPPINGS")
                        if valid_py:
                            node_info[filename] = f"Name {filename} is valid!"
                        else:
                            node_info[filename] = f"Name {filename} invalid. Missing attribute mappings"

                    elif scan_mode == "Check Libraries":
                        source_code = inspect.getsource(module)
                        tree = ast.parse(source_code)                       
                        imported_modules = []
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.Import, ast.ImportFrom)):
                                for alias in node.names:
                                    imported_modules.append(alias.name)
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

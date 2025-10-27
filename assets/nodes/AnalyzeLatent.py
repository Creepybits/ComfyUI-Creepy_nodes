
import math
import copy
import torch
import torch.nn.functional as F
import numpy as np
import cv2
from pymatting import estimate_alpha_cf, estimate_foreground_ml, fix_trimap
from tqdm import trange

try:
    from cv2.ximgproc import guidedFilter
except ImportError:
    print("\033[33mUnable to import guidedFilter, make sure you have only opencv-contrib-python or run the import_error_install.bat script\033[m")

import comfy.model_management
import node_helpers
from comfy.utils import ProgressBar
from comfy_extras.nodes_post_processing import gaussian_kernel

class AnalyzeLatent:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"latent": ("LATENT", ),}}

    RETURN_TYPES = ("STRING", "FLOAT", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("stats", "c0_mean", "c1_mean", "c2_mean", "c3_mean")
    FUNCTION = "notify"
    OUTPUT_NODE = True
    CATEGORY = "Creepybits/experimental"

    def notify(self, latent):
        latents = latent["samples"]
        channels = latents.size(1)
        width, height = latents.size(3), latents.size(2)

        text = ["",]
        text[0] = f"batch size: {latents.size(0)}"
        text.append(f"channels: {channels}")
        text.append(f"width: {width} ({width * 8})")
        text.append(f"height: {height} ({height * 8})")

        cmean = [0,0,0,0]
        for i in range(channels):
            minimum = torch.min(latents[:,i,:,:]).item()
            maximum = torch.max(latents[:,i,:,:]).item()
            std_dev, mean = torch.std_mean(latents[:,i,:,:], dim=None)
            if i < 4:
                cmean[i] = mean

            text.append(f"c{i} mean: {mean:.1f} std_dev: {std_dev:.1f} min: {minimum:.1f} max: {maximum:.1f}")


        printtext = "\033[36mLatent Stats:\033[m"
        for t in text:
            printtext += "\n    " + t

        returntext = ""
        for i in range(len(text)):
            if i > 0:
                returntext += "\n"
            returntext += text[i]

        print(printtext)
        return (returntext, cmean[0], cmean[1], cmean[2], cmean[3])


NODE_CLASS_MAPPINGS = {
    "Analyze Latent": AnalyzeLatent,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnalyzeLatent": "Analyze Latent (Creepybits)",
}

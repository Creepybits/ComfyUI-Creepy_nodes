import os
import sys
import subprocess
import argostranslate.package
import argostranslate.translate

# Add the path to your custom nodes directory to the Python path
# If this isn't done, Python won't be able to find your custom node modules
custom_nodes_path = os.path.dirname(os.path.abspath(__file__))
assets_nodes_path = os.path.join(custom_nodes_path, "assets", "nodes") #New
sys.path.append(assets_nodes_path) #New

from .assets.nodes.Modelswitch import NODE_CLASS_MAPPINGS as Modelswitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Modelswitch_NODE_DISPLAY_NAMES
from .assets.nodes.VAESwitch import NODE_CLASS_MAPPINGS as VAESwitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VAESwitch_NODE_DISPLAY_NAMES
from .assets.nodes.CLIPSwitch import NODE_CLASS_MAPPINGS as CLIPSwitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CLIPSwitch_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicModelswitch import NODE_CLASS_MAPPINGS as DynamicModelswitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicModelswitch_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicClipswitch import NODE_CLASS_MAPPINGS as DynamicClipswitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicClipswitch_NODE_DISPLAY_NAMES
from .assets.nodes.Textswitch import NODE_CLASS_MAPPINGS as Textswitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Textswitch_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicConditioning import NODE_CLASS_MAPPINGS as DynamicConditioning_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicConditioning_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicLatentSwitch import NODE_CLASS_MAPPINGS as DynamicLatentSwitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicLatentSwitch_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicVAESwitch import NODE_CLASS_MAPPINGS as DynamicVAESwitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicVAESwitch_NODE_DISPLAY_NAMES
from .assets.nodes.SystemPromp import NODE_CLASS_MAPPINGS as SystemPromp_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SystemPromp_NODE_DISPLAY_NAMES
from .assets.nodes.DelayNode import NODE_CLASS_MAPPINGS as DelayNode_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DelayNode_NODE_DISPLAY_NAMES
from .assets.nodes.DelayTextNode import NODE_CLASS_MAPPINGS as DelayTextNode_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DelayTextNode_NODE_DISPLAY_NAMES
from .assets.nodes.SanitizeFilename import NODE_CLASS_MAPPINGS as SanitizeFilename_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SanitizeFilename_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicImageSwitch import NODE_CLASS_MAPPINGS as DynamicImageSwitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicImageSwitch_NODE_DISPLAY_NAMES
from .assets.nodes.EvaluaterNode import NODE_CLASS_MAPPINGS as EvaluaterNode_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as EvaluaterNode_NODE_DISPLAY_NAMES
from .assets.nodes.PeopleEvaluationNode import NODE_CLASS_MAPPINGS as PeopleEvaluationNode_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as PeopleEvaluationNode_NODE_DISPLAY_NAMES
from .assets.nodes.ArgosTranslateNode import NODE_CLASS_MAPPINGS as ArgosTranslateNode_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ArgosTranslateNode_NODE_DISPLAY_NAMES
from .assets.nodes.CustomNodeManager import NODE_CLASS_MAPPINGS as CustomNodeManager_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CustomNodeManager_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicDelayText import NODE_CLASS_MAPPINGS as DynamicDelayText_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicDelayText_NODE_DISPLAY_NAMES
from .assets.nodes.CollectAndDistributeText import NODE_CLASS_MAPPINGS as CollectAndDistributeText_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CollectAndDistributeText_NODE_DISPLAY_NAMES
from .assets.nodes.PromptGenerator import NODE_CLASS_MAPPINGS as PromptGenerator_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as PromptGenerator_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.KeywordExtractor import NODE_CLASS_MAPPINGS as KeywordExtractor_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as KeywordExtractor_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.SummaryWriter import NODE_CLASS_MAPPINGS as SummaryWriter_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SummaryWriter_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.FilterImages import NODE_CLASS_MAPPINGS as FilterImages_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as FilterImages_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.LoadBatchImagesDir import NODE_CLASS_MAPPINGS as LoadBatchImagesDir_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoadBatchImagesDir_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.GeminiAPI import NODE_CLASS_MAPPINGS as GeminiAPI_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as GeminiAPI_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.GeminiAudioAnalyzer import NODE_CLASS_MAPPINGS as GeminiAudioAnalyzer_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as GeminiAudioAnalyzer_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.RandomAudioSegment import NODE_CLASS_MAPPINGS as RandomAudioSegment_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as RandomAudioSegment_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.AudioKeywordExtractor import NODE_CLASS_MAPPINGS as AudioKeywordExtractor_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AudioKeywordExtractor_NODE_DISPLAY_NAME_MAPPINGS


import comfy.sd
import comfy.utils
import time
import re
import json

# Try to import folder_paths from ComfyUI
try:
    import folder_paths
except ImportError:
    print("Warning: Could not import folder_paths from ComfyUI")
    folder_paths = None

NODE_CLASS_MAPPINGS = {
    **Modelswitch_NODE_MAPPINGS,
    **VAESwitch_NODE_MAPPINGS,
    **CLIPSwitch_NODE_MAPPINGS,
    **DynamicModelswitch_NODE_MAPPINGS,
    **DynamicClipswitch_NODE_MAPPINGS,
    **Textswitch_NODE_MAPPINGS,
    **DynamicConditioning_NODE_MAPPINGS,
    **DynamicLatentSwitch_NODE_MAPPINGS,
    **DynamicVAESwitch_NODE_MAPPINGS,
    **SystemPromp_NODE_MAPPINGS,
    **DelayNode_NODE_MAPPINGS,
    **DelayTextNode_NODE_MAPPINGS,
    **SanitizeFilename_NODE_MAPPINGS,
    **DynamicImageSwitch_NODE_MAPPINGS,
    **EvaluaterNode_NODE_MAPPINGS,
    **PeopleEvaluationNode_NODE_MAPPINGS,
    **ArgosTranslateNode_NODE_MAPPINGS,
    **CustomNodeManager_NODE_MAPPINGS,
    **DynamicDelayText_NODE_MAPPINGS,
    **CollectAndDistributeText_NODE_CLASS_MAPPINGS,
    **PromptGenerator_NODE_CLASS_MAPPINGS,
    **KeywordExtractor_NODE_CLASS_MAPPINGS,
    **SummaryWriter_NODE_CLASS_MAPPINGS,
    **FilterImages_NODE_CLASS_MAPPINGS,
    **LoadBatchImagesDir_NODE_CLASS_MAPPINGS,
    **GeminiAPI_NODE_CLASS_MAPPINGS,
    **GeminiAudioAnalyzer_NODE_CLASS_MAPPINGS,
    **RandomAudioSegment_NODE_CLASS_MAPPINGS,
    **AudioKeywordExtractor_NODE_CLASS_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **Modelswitch_NODE_DISPLAY_NAMES,
    **VAESwitch_NODE_DISPLAY_NAMES,
    **CLIPSwitch_NODE_DISPLAY_NAMES,
    **DynamicModelswitch_NODE_DISPLAY_NAMES,
    **DynamicClipswitch_NODE_DISPLAY_NAMES,
    **Textswitch_NODE_DISPLAY_NAMES,
    **DynamicConditioning_NODE_DISPLAY_NAMES,
    **DynamicLatentSwitch_NODE_DISPLAY_NAMES,
    **DynamicVAESwitch_NODE_DISPLAY_NAMES,
    **SystemPromp_NODE_DISPLAY_NAMES,
    **DelayNode_NODE_DISPLAY_NAMES,
    **DelayTextNode_NODE_DISPLAY_NAMES,
    **SanitizeFilename_NODE_DISPLAY_NAMES,
    **DynamicImageSwitch_NODE_DISPLAY_NAMES,
    **EvaluaterNode_NODE_DISPLAY_NAMES,
    **PeopleEvaluationNode_NODE_DISPLAY_NAMES,
    **ArgosTranslateNode_NODE_DISPLAY_NAMES,
    **CustomNodeManager_NODE_DISPLAY_NAMES,
    **DynamicDelayText_NODE_DISPLAY_NAMES,
    **CollectAndDistributeText_NODE_DISPLAY_NAMES,
    **PromptGenerator_NODE_DISPLAY_NAME_MAPPINGS,
    **KeywordExtractor_NODE_DISPLAY_NAME_MAPPINGS,
    **SummaryWriter_NODE_DISPLAY_NAME_MAPPINGS,
    **FilterImages_NODE_DISPLAY_NAME_MAPPINGS,
    **LoadBatchImagesDir_NODE_DISPLAY_NAME_MAPPINGS,
    **GeminiAPI_NODE_DISPLAY_NAME_MAPPINGS,
    **GeminiAudioAnalyzer_NODE_DISPLAY_NAME_MAPPINGS,
    **RandomAudioSegment_NODE_DISPLAY_NAME_MAPPINGS,
    **AudioKeywordExtractor_NODE_DISPLAY_NAME_MAPPINGS,
}

__version__ = "2.2.6"

# Define the web directory for ComfyUI to find our JavaScript files
WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

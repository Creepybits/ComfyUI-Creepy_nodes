import os
import sys
import subprocess 


# Add the path to your custom nodes directory to the Python path
custom_nodes_path = os.path.dirname(os.path.abspath(__file__))
assets_nodes_path = os.path.join(custom_nodes_path, "assets", "nodes")
sys.path.append(assets_nodes_path)

# --- IMPORT ALL YOUR NODES FROM assets/nodes ---
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
from .assets.nodes.ModelBridge import NODE_CLASS_MAPPINGS as ModelBridge_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ModelBridge_NODE_DISPLAY_NAMES
from .assets.nodes.WANModelBridge import NODE_CLASS_MAPPINGS as WANModelBridge_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as WANModelBridge_NODE_DISPLAY_NAMES
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
from .assets.nodes.IMGToIMGConditioning import NODE_CLASS_MAPPINGS as IMGToIMGConditioning_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as IMGToIMGConditioning_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.Coloring import NODE_CLASS_MAPPINGS as Coloring_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Coloring_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.Categorizer import NODE_CLASS_MAPPINGS as Categorizer_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Categorizer_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.conditional_lora_selector import NODE_CLASS_MAPPINGS as ConditionalLoRAApplier_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ConditionalLoRAApplier_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.UnifiedModelBridge import NODE_CLASS_MAPPINGS as UnifiedModelBridge_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as UnifiedModelBridge_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.VaceToVideoAdvanced import NODE_CLASS_MAPPINGS as VaceToVideoAdvanced_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VaceToVideoAdvanced_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.MasterKey import NODE_CLASS_MAPPINGS as MasterKey_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as MasterKey_NODE_DISPLAY_NAME_MAPPINGS



import comfy.sd # Keep if needed by any nodes
import comfy.utils # Keep if needed by any nodes
import time # Keep if needed by any nodes
import re # Keep if needed by any nodes
import json # Keep if needed by any nodes

# Try to import folder_paths from ComfyUI
try:
    import folder_paths
except ImportError:
    print("Warning: Could not import folder_paths from ComfyUI")
    folder_paths = None

# --- CONSOLIDATE ALL NODE MAPPINGS ---
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
    **ModelBridge_NODE_MAPPINGS,
    **WANModelBridge_NODE_MAPPINGS, # Keep commented
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
    **IMGToIMGConditioning_NODE_CLASS_MAPPINGS,
    **Coloring_NODE_CLASS_MAPPINGS,
    **Categorizer_NODE_CLASS_MAPPINGS,
    **UnifiedModelBridge_NODE_CLASS_MAPPINGS, # <--- ADD THIS LINE
    **ConditionalLoRAApplier_NODE_CLASS_MAPPINGS,
    **VaceToVideoAdvanced_NODE_CLASS_MAPPINGS,
    **MasterKey_NODE_CLASS_MAPPINGS,
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
    **ModelBridge_NODE_DISPLAY_NAMES,
    **WANModelBridge_NODE_DISPLAY_NAMES, # Keep commented
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
    **IMGToIMGConditioning_NODE_DISPLAY_NAME_MAPPINGS,
    **Coloring_NODE_DISPLAY_NAME_MAPPINGS,
    **Categorizer_NODE_DISPLAY_NAME_MAPPINGS,
    **UnifiedModelBridge_NODE_DISPLAY_NAME_MAPPINGS, # <--- ADD THIS LINE
    **ConditionalLoRAApplier_NODE_DISPLAY_NAME_MAPPINGS,
    **VaceToVideoAdvanced_NODE_DISPLAY_NAME_MAPPINGS,
    **MasterKey_NODE_DISPLAY_NAME_MAPPINGS,
}

__version__ = "2.4.2" # Update this version if you like

# Define the web directory for ComfyUI to find our JavaScript files
WEB_DIRECTORY = "./web" # This points to ComfyUI/custom_nodes/Creepy_nodes/web

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print("-------------------------------------------------------------------")
print("Thank you for using Creepybits Custom Nodes! - Nova was here, probably looking for snacks.")
print("Loading nodes:")
for node_name in NODE_CLASS_MAPPINGS.keys():
    print(f"  - {node_name}")
if 'WEB_DIRECTORY' in locals():
    print(f"Web directory for custom UI: {WEB_DIRECTORY}")
print("-------------------------------------------------------------------")

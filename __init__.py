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
from .assets.nodes.QWENPrompt import NODE_CLASS_MAPPINGS as QWENPrompt_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as QWENPrompt_NODE_DISPLAY_NAMES
from .assets.nodes.creepy_directors_slate import NODE_CLASS_MAPPINGS as creepy_directors_slate_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as creepy_directors_slate_NODE_DISPLAY_NAMES
from .assets.nodes.CustomNodeManager import NODE_CLASS_MAPPINGS as CustomNodeManager_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CustomNodeManager_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicDelayText import NODE_CLASS_MAPPINGS as DynamicDelayText_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicDelayText_NODE_DISPLAY_NAMES
from .assets.nodes.CollectAndDistributeText import NODE_CLASS_MAPPINGS as CollectAndDistributeText_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CollectAndDistributeText_NODE_DISPLAY_NAMES
from .assets.nodes.KeywordExtractor import NODE_CLASS_MAPPINGS as KeywordExtractor_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as KeywordExtractor_NODE_DISPLAY_NAMES
from .assets.nodes.SummaryWriter import NODE_CLASS_MAPPINGS as SummaryWriter_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SummaryWriter_NODE_DISPLAY_NAMES
from .assets.nodes.FilterImages import NODE_CLASS_MAPPINGS as FilterImages_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as FilterImages_NODE_DISPLAY_NAMES
from .assets.nodes.LoadBatchImagesDir import NODE_CLASS_MAPPINGS as LoadBatchImagesDir_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoadBatchImagesDir_NODE_DISPLAY_NAMES
from .assets.nodes.GeminiAPI import NODE_CLASS_MAPPINGS as GeminiAPI_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as GeminiAPI_NODE_DISPLAY_NAMES
from .assets.nodes.GeminiAudioAnalyzer import NODE_CLASS_MAPPINGS as GeminiAudioAnalyzer_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as GeminiAudioAnalyzer_NODE_DISPLAY_NAMES
from .assets.nodes.RandomAudioSegment import NODE_CLASS_MAPPINGS as RandomAudioSegment_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as RandomAudioSegment_NODE_DISPLAY_NAMES
from .assets.nodes.AudioKeywordExtractor import NODE_CLASS_MAPPINGS as AudioKeywordExtractor_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AudioKeywordExtractor_NODE_DISPLAY_NAMES
from .assets.nodes.IMGToIMGConditioning import NODE_CLASS_MAPPINGS as IMGToIMGConditioning_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as IMGToIMGConditioning_NODE_DISPLAY_NAMES
from .assets.nodes.Coloring import NODE_CLASS_MAPPINGS as Coloring_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Coloring_NODE_DISPLAY_NAMES
from .assets.nodes.Categorizer import NODE_CLASS_MAPPINGS as Categorizer_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as Categorizer_NODE_DISPLAY_NAMES
from .assets.nodes.conditional_lora_selector import NODE_CLASS_MAPPINGS as ConditionalLoRAApplier_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ConditionalLoRAApplier_NODE_DISPLAY_NAMES
from .assets.nodes.LoadBatchFromDir import NODE_CLASS_MAPPINGS as LoadBatchFromDir_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoadBatchFromDir_NODE_DISPLAY_NAMES
from .assets.nodes.WanPrompter import NODE_CLASS_MAPPINGS as WanPrompter_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as WanPrompter_NODE_DISPLAY_NAMES
from .assets.nodes.MasterKey import NODE_CLASS_MAPPINGS as MasterKey_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as MasterKey_NODE_DISPLAY_NAMES
from .assets.nodes.ArtAnalyst import NODE_CLASS_MAPPINGS as ArtAnalyst_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ArtAnalyst_NODE_DISPLAY_NAMES
from .assets.nodes.SceneDirector import NODE_CLASS_MAPPINGS as SceneDirector_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SceneDirector_NODE_DISPLAY_NAMES
from .assets.nodes.DynamicStartIndex import NODE_CLASS_MAPPINGS as DynamicStartIndex_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as DynamicStartIndex_NODE_DISPLAY_NAMES
from .assets.nodes.LoadVideoPath import NODE_CLASS_MAPPINGS as LoadVideoPath_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoadVideoPath_NODE_DISPLAY_NAMES
from .assets.nodes.FallbackTextSwitch import NODE_CLASS_MAPPINGS as FallbackTextSwitch_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as FallbackTextSwitch_NODE_DISPLAY_NAMES
from .assets.nodes.AnalyzeLatent import NODE_CLASS_MAPPINGS as AnalyzeLatent_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as AnalyzeLatent_NODE_DISPLAY_NAMES
from .assets.nodes.RebuildLatent import NODE_CLASS_MAPPINGS as RebuildLatent_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as RebuildLatent_NODE_DISPLAY_NAMES
from .assets.nodes.VideoCombineSeparateAlpha import NODE_CLASS_MAPPINGS as VideoCombineSeparateAlpha_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as VideoCombineSeparateAlpha_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.latent import NODE_CLASS_MAPPINGS as LoadLatentFromPath_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoadLatentFromPath_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.latent import NODE_CLASS_MAPPINGS as SaveRawLatent_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SaveRawLatent_NODE_DISPLAY_NAME_MAPPINGS
from .assets.nodes.QwenAspectRatio import NODE_CLASS_MAPPINGS as QwenAspectRatio_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as QwenAspectRatio_NODE_DISPLAY_NAMES
from .assets.nodes.LoraTriggerLookup import NODE_CLASS_MAPPINGS as LoraTriggerLookup_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraTriggerLookup_NODE_DISPLAY_NAMES
from .assets.nodes.LoraDBBuilder import NODE_CLASS_MAPPINGS as LoraDBBuilder_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as LoraDBBuilder_NODE_DISPLAY_NAMES
from .assets.nodes.MediaMigratorNode import NODE_CLASS_MAPPINGS as MediaMigratorNode_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as MediaMigratorNode_DISPLAY_NAMES
from .assets.nodes.EmptyFolderCleanerNode import NODE_CLASS_MAPPINGS as EmptyFolderCleanerNode_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as EmptyFolderCleanerNode_DISPLAY_NAMES
from .assets.nodes.FileSorterNode import NODE_CLASS_MAPPINGS as FileSorterNode_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as FileSorterNode_DISPLAY_NAMES
from .assets.nodes.ImageFormatConverter import NODE_CLASS_MAPPINGS as ImageFormatConverter_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as ImageFormatConverter_NODE_DISPLAY_NAME_MAPPINGS



import comfy.sd 
import comfy.utils 
import time 
import re 
import json 


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
    **QWENPrompt_NODE_MAPPINGS,
    **creepy_directors_slate_NODE_MAPPINGS,
    **CustomNodeManager_NODE_MAPPINGS,
    **DynamicDelayText_NODE_MAPPINGS,
    **CollectAndDistributeText_NODE_MAPPINGS,
    **KeywordExtractor_NODE_MAPPINGS,
    **SummaryWriter_NODE_MAPPINGS,
    **FilterImages_NODE_MAPPINGS,
    **LoadBatchImagesDir_NODE_MAPPINGS,
    **GeminiAPI_NODE_MAPPINGS,
    **GeminiAudioAnalyzer_NODE_MAPPINGS,
    **RandomAudioSegment_NODE_MAPPINGS,
    **AudioKeywordExtractor_NODE_MAPPINGS,
    **IMGToIMGConditioning_NODE_MAPPINGS,
    **Coloring_NODE_MAPPINGS,
    **Categorizer_NODE_MAPPINGS,
    **LoadBatchFromDir_NODE_MAPPINGS, # <--- ADD THIS LINE
    **ConditionalLoRAApplier_NODE_MAPPINGS,
    **WanPrompter_NODE_MAPPINGS,
    **MasterKey_NODE_MAPPINGS,
    **ArtAnalyst_NODE_MAPPINGS,
    **SceneDirector_NODE_MAPPINGS,
    **DynamicStartIndex_NODE_MAPPINGS,
    **LoadVideoPath_NODE_MAPPINGS,
    **FallbackTextSwitch_NODE_MAPPINGS,
    **AnalyzeLatent_NODE_MAPPINGS,
    **RebuildLatent_NODE_MAPPINGS,
    **VideoCombineSeparateAlpha_NODE_CLASS_MAPPINGS,
    **LoadLatentFromPath_NODE_CLASS_MAPPINGS,
    **SaveRawLatent_NODE_CLASS_MAPPINGS,
    **QwenAspectRatio_NODE_MAPPINGS,
    **LoraTriggerLookup_NODE_MAPPINGS,
    **LoraDBBuilder_NODE_MAPPINGS,
    **MediaMigratorNode_MAPPINGS,
    **EmptyFolderCleanerNode_MAPPINGS,
    **FileSorterNode_MAPPINGS,
    **ImageFormatConverter_NODE_CLASS_MAPPINGS,

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
    **QWENPrompt_NODE_DISPLAY_NAMES,
    **creepy_directors_slate_NODE_DISPLAY_NAMES,
    **CustomNodeManager_NODE_DISPLAY_NAMES,
    **DynamicDelayText_NODE_DISPLAY_NAMES,
    **CollectAndDistributeText_NODE_DISPLAY_NAMES,
    **KeywordExtractor_NODE_DISPLAY_NAMES,
    **SummaryWriter_NODE_DISPLAY_NAMES,
    **FilterImages_NODE_DISPLAY_NAMES,
    **LoadBatchImagesDir_NODE_DISPLAY_NAMES,
    **GeminiAPI_NODE_DISPLAY_NAMES,
    **GeminiAudioAnalyzer_NODE_DISPLAY_NAMES,
    **RandomAudioSegment_NODE_DISPLAY_NAMES,
    **AudioKeywordExtractor_NODE_DISPLAY_NAMES,
    **IMGToIMGConditioning_NODE_DISPLAY_NAMES,
    **Coloring_NODE_DISPLAY_NAMES,
    **Categorizer_NODE_DISPLAY_NAMES,
    **LoadBatchFromDir_NODE_DISPLAY_NAMES, # <--- ADD THIS LINE
    **ConditionalLoRAApplier_NODE_DISPLAY_NAMES,
    **WanPrompter_NODE_DISPLAY_NAMES,
    **MasterKey_NODE_DISPLAY_NAMES,
    **ArtAnalyst_NODE_DISPLAY_NAMES,
    **SceneDirector_NODE_DISPLAY_NAMES,
    **DynamicStartIndex_NODE_DISPLAY_NAMES,
    **LoadVideoPath_NODE_DISPLAY_NAMES,
    **FallbackTextSwitch_NODE_DISPLAY_NAMES,
    **AnalyzeLatent_NODE_DISPLAY_NAMES,
    **RebuildLatent_NODE_DISPLAY_NAMES,
    **VideoCombineSeparateAlpha_NODE_DISPLAY_NAME_MAPPINGS,
        **LoadLatentFromPath_NODE_DISPLAY_NAME_MAPPINGS,
    **SaveRawLatent_NODE_DISPLAY_NAME_MAPPINGS,
    **QwenAspectRatio_NODE_DISPLAY_NAMES,
    **LoraTriggerLookup_NODE_DISPLAY_NAMES,
    **LoraDBBuilder_NODE_DISPLAY_NAMES,
    **MediaMigratorNode_DISPLAY_NAMES,
    **EmptyFolderCleanerNode_DISPLAY_NAMES,
    **FileSorterNode_DISPLAY_NAMES,
    **ImageFormatConverter_NODE_DISPLAY_NAME_MAPPINGS,
}

__version__ = "2.5.4" 


WEB_DIRECTORY = "./web" 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

print("-------------------------------------------------------------------")
print("Thank you for using Creepybits Custom Nodes! - Nova was here, probably looking for snacks.")
print("Loading nodes:")
for node_name in NODE_CLASS_MAPPINGS.keys():
    print(f"  - {node_name}")
if 'WEB_DIRECTORY' in locals():
    print(f"Web directory for custom UI: {WEB_DIRECTORY}")
print("-------------------------------------------------------------------")







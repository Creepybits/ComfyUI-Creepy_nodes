

🎨 Coloring Node
A unique utility that uses an AI to analyze and generate a descriptive text about the color palette, mood, and tones of an input image.

Philosophy & Use Case: The Coloring Node acts as your personal AI color theorist. It's designed to go beyond simple color picking by providing a rich, descriptive analysis of an image's color scheme. You provide an image, and the node uses a powerful multimodal AI to "see" the colors and describe them in natural language. This is perfect for artists who want to understand the emotional impact of a color palette, generate color-related keywords for a new prompt, or simply find the right words to describe a specific aesthetic.

General Usage:

color_image: This is the primary input for the image you want the AI to analyze.

system_prompt: This is where you give the AI its instructions. You can ask it to do anything from "Describe the dominant colors and overall mood of this image" to "Write a short poem inspired by this color palette."

ref_image (optional): You can provide a second image for comparison or additional context.

The node outputs a text string containing the AI's complete analysis, ready to be used for inspiration or as part of a new prompt.

<img width="505" height="447" alt="image" src="https://github.com/user-attachments/assets/8c4485f8-00ff-4919-bfe0-a950028c5305" />


## 🎨 Qwen Aspect Ratio
A simple but essential utility that provides a dropdown menu of the officially supported aspect ratios for the Qwen family of models.

Philosophy & Use Case: The Qwen models are incredibly powerful, but they are trained to perform best at a specific, non-standard set of resolutions. Generating outside these resolutions can lead to artifacts or poor compositions. This node eliminates the need to memorize or look up those values. It acts as a "preset manager," providing a simple dropdown of familiar aspect ratios (like "16:9" or "4:3") and outputting the exact, Qwen-compliant width and height for your workflow.

General Usage:

ratio: Select your desired aspect ratio from the dropdown menu.

The node will output the corresponding width and height integers, which you should connect to your "Empty Latent Image" node or any other input that defines your generation's dimensions.

<img width="355" height="300" alt="image" src="https://github.com/user-attachments/assets/3ff60f23-fa83-47df-aa88-ac3bed2735aa" />




## 🎨 Save Raw Latent
An advanced utility for saving the raw latent representation of an image directly to a file, preserving the exact state for later use.

Philosophy & Use Case: This node is for advanced, non-destructive workflows. It allows you to save the "digital DNA" of a generation before it gets decoded into a final image. This is incredibly powerful for experimenting with different VAEs, upscaling techniques, or decoding settings on the exact same base generation without having to re-run the entire sampling process. It saves time and ensures perfect consistency.

General Usage:

samples: Connect the LATENT output from your KSampler to this input.

folder_path / filename: Specify where you want to save the .latent file within your ComfyUI output directory.

<img width="287" height="156" alt="image" src="https://github.com/user-attachments/assets/884d6e17-eae0-4e3c-be03-e061e5191301" />


## 🎨 Load Latent From Path
An advanced utility for loading a raw .latent file directly from your file system, perfectly restoring a previous generation's state.

Philosophy & Use Case: This is the companion node to the Save Raw Latent node. It allows you to load a previously saved latent file, bypassing the need for a text prompt, checkpoint loader, or KSampler. It's the starting point for any workflow where you want to experiment on a specific, saved generation.

General Usage:

latent_path: Provide the path to your .latent file. Note that this path is relative to your ComfyUI root directory, not just the output folder.

The node outputs a LATENT that can be directly connected to a VAE Decode node to produce an image.

<img width="376" height="152" alt="image" src="https://github.com/user-attachments/assets/710245a3-7e3d-4a45-a085-e8fd34da4359" />


## 🎨 LoRA DB Builder
An automated utility that interrogates the Civitai database to find the official trigger words for your LoRA files and saves them to a local database for instant recall.

Philosophy & Use Case: The LoRA DB Builder is your personal LoRA librarian. It solves the universal problem of forgetting or having to manually look up the specific trigger words needed to activate a LoRA. It works by calculating a unique fingerprint (a SHA256 hash) of your selected LoRA file, asking Civitai's API, "Have you seen this file before, and what are its trigger words?", and then saving the answer in a local lora_triggers.json file. This builds a permanent, local "cheat sheet" for your entire LoRA collection, saving you an enormous amount of time and effort.

General Usage:

lora_name: Select the LoRA you want to look up from the dropdown menu, which automatically scans all your LoRA folders.

force_fetch: A toggle to force the node to re-check with Civitai, even if it already has an entry in its local database. This is useful if a model page has been updated.

The node outputs a found_trigger_words string, which you can then copy into your prompt or connect to another node.

<img width="437" height="245" alt="image" src="https://github.com/user-attachments/assets/251e9984-e703-42c5-a78f-7e8a67b9e711" />

## 🎨 LoRA Trigger Lookup
A fast and simple utility to instantly retrieve the trigger words for any LoRA in your collection from your local database.

Philosophy & Use Case: This node is the "quick reference" companion to the LoRA DB Builder. Once you've used the builder to create your lora_triggers.json database, this node provides instant access to it. It's designed to be a simple, efficient part of your daily workflow. Instead of having to remember trigger words, you simply select your LoRA from the dropdown, and this node outputs the correct words, ready to be connected to your prompt.

General Usage:

lora_name: Select the LoRA you want from the dropdown list.

num_triggers: Control how many of the stored trigger words you want to output. A value of -1 will output all of them.

delimiter: A string (like , ) that will be placed between the trigger words in the final output string.

The node outputs a clean trigger_words string, ready to be combined with your main prompt.

<img width="439" height="225" alt="image" src="https://github.com/user-attachments/assets/6343d60b-7d72-41f0-9587-27c1eab567d1" />

## 🎨 Random/Fixed Audio Picker
A dual-mode utility for extracting audio segments, allowing you to either grab a random snippet or precisely clip a section from a specific start time.

Philosophy & Use Case: This node is your audio sampling tool. It's designed for two distinct purposes. In its "random" mode, it's a creative engine, perfect for pulling unpredictable sound bites from a larger audio file to generate inspiration or create variations. In its "fixed" mode, it's a precision editing tool, allowing you to extract an exact segment (e.g., "the 10 seconds of audio starting at the 1:30 mark") without needing an external editor.

General Usage:

audio: Connect the source audio you want to sample from.

segment_length: Specify the duration in seconds of the clip you want to extract.

start_time: This is the control that switches the node's mode.

If left at the default of -1.0, the node will pick a random start time.

If you enter a specific value (e.g., 90.0), the node will start the clip exactly at that time (90 seconds in).

<img width="491" height="237" alt="image" src="https://github.com/user-attachments/assets/42f87ac7-c798-4c4f-aafd-93ae74c4deb5" />

## 🎨 System Prompt
A utility for loading a pre-written system prompt from a text file and combining it with a dynamic prompt from your workflow.

Philosophy & Use Case: The System Prompt node is a simple but powerful organizational tool. Its purpose is to keep your workflows clean by externalizing large, reusable blocks of text. Instead of having a massive, multi-line system prompt taking up space on your canvas, you can save it in a dedicated system_prompt.txt file within the node's assets folder. This node then automatically loads that file and combines its content with any dynamic text you provide (like the output from a Master Key node). This is perfect for reusing the same complex instructions across multiple projects and editing them in one central place.

General Usage: The node has one input for your dynamic text (text_2). It automatically loads the content from .../prompts/system_prompt.txt and prepends it to your input text, outputting a single, combined string ready for an LLM.

<img width="520" height="372" alt="image" src="https://github.com/user-attachments/assets/aabc3883-c435-496f-b36a-6474249b58c0" />

## 🎨 Custom Node Manager
A powerful diagnostic utility for developers, designed to scan a directory of custom nodes and report on their validity and dependencies.

Philosophy & Use Case: The Custom Node Manager is your quality control inspector and librarian for your entire node collection. It's a "meta-node" that looks at the Python files of your other nodes to help you manage and debug them. It's not used in a typical image generation workflow, but rather as a developer's tool to ensure all your nodes are correctly formatted and to quickly see what external libraries they rely on.

General Usage: The node has two primary modes, selected via the scan_mode dropdown:

Validate Python mode: In this mode, the node acts as a quality control inspector. It checks every Python file in the target directory to see if it contains the essential NODE_CLASS_MAPPINGS. This is the fundamental requirement for a Python file to be recognized by ComfyUI as a valid custom node. It will give you a report of which files are valid and which are not.

Check Libraries mode: In this mode, the node acts as a librarian. It reads the source code of each Python file and generates a list of all the external libraries that the node imports. This is incredibly useful for creating requirements.txt files or for troubleshooting ModuleNotFoundError errors by quickly seeing exactly what dependencies a node has.


<img width="534" height="247" alt="image" src="https://github.com/user-attachments/assets/a66ca735-27b5-4725-bd80-ee0e404d5d75" />




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



Lora DB Builder / Lora Trigger Lookup: Your Lora management suite for organizing and accessing trigger words.

Random Audio Segment: A creative utility for pulling random snippets from a larger audio file.

Creepy CLIP Loader: A custom loader for specialized CLIP models.

System Prompt: A utility for loading and managing system prompts from text files.

Custom Node Manager: The meta-node for managing the entire suite!

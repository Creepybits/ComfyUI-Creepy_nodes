## ⚙️ Conditional LoRA Applier
An intelligent node that automatically applies the correct LoRAs to your model and CLIP based on keywords found in your prompt.

Philosophy & Use Case: The Conditional LoRA Applier is your automated workflow director. Its purpose is to eliminate the need for complex switches or manually changing LoRAs every time you change your prompt. You create a simple "rulebook" that tells the node, "If you see the word 'portrait' in the prompt, apply my favorite portrait LoRA." This allows you to build universal, "set-it-and-forget-it" workflows that intelligently adapt to your creative ideas. It can apply multiple LoRAs if multiple rules are met, and even apply a default "house style" LoRA if no other rules match.

General Usage: The node takes your main model and clip as inputs. Its logic is controlled by two main text boxes:

prompt: This is where you connect the text prompt you intend to use for generation. The node reads this text to look for your keywords.

lora_definitions: This is your "rulebook." You define your rules here, one per line, using a simple format. The node includes helpful comments explaining exactly how to write them. The basic format is:

keyword1, keyword2 : path/to/your/lora.safetensors, model_strength, clip_strength

Default LoRA: You can use the dropdowns to select a default_lora_name that will be applied automatically only if no keywords from your rulebook are found in the prompt. This is perfect for setting a general style.

<img width="1338" height="673" alt="image" src="https://github.com/user-attachments/assets/50bc9c02-5c9a-446f-b465-d90a9b1f4937" />


## ⚙️ Switch Nodes (Dynamic & Multi)
A suite of essential logic nodes that act as routers, allowing you to dynamically change the flow of data (models, images, latents, etc.) within your workflow without any rewiring.

Philosophy & Use Case: Switch nodes are the traffic directors of your ComfyUI workflows. Their purpose is to give you control over the path your data takes. They are perfect for A/B testing different models, creating workflows with multiple "modes" (e.g., an "SDXL" mode that uses one set of models and a "FLUX" mode that uses another), or building complex conditional logic. They replace the need to manually connect and disconnect noodles every time you want to experiment.

General Usage: The principle is simple: connect your different options (e.g., three different checkpoints) to the inputs (model1, model2, model3). Then, use the integer Input selector widget to choose which one (1, 2, or 3) gets passed out of the main MODEL output. This allows you to switch between them with a single click. The "Dynamic" versions often allow for a variable number of inputs that can be selected programmatically.

The Suite Includes:

Model Switches: Dynamic Model Switch, Multi Model Switch

CLIP Switches: Dynamic Clip Switch, Multi CLIP Switch

VAE Switches: Dynamic VAE Switch, Multi VAE Switch

Image Switches: Dynamic Image Switch

Latent Switches: Dynamic Latent Switch

Conditioning Switches: Dynamic Conditioning

<img width="955" height="403" alt="image" src="https://github.com/user-attachments/assets/27561ee2-5b7f-4e7f-a9c5-13c11aec614a" />


## ⚙️ Delay Nodes
A suite of utility nodes designed to control the timing and flow of data by introducing a pause into the workflow.

Philosophy & Use Case: Delay nodes are the pacemakers of your workflow. Their primary purpose is to control the sequence of events, ensuring that one process has time to complete before another begins, or simply to add a timed interval between actions.

The Suite Includes:

Delay Node / Delay Text Node: These are simple, "blocking" delays. Think of them as a red light in your workflow. When data (an image or text) arrives, the node holds it for the specified number of seconds, pausing everything downstream. After the timer completes, it releases the data and the workflow continues. They are perfect for simple sequencing.

Dynamic Delay Text: This is a more advanced "debouncer" node. It's not designed to just pause, but to wait for a pause in a stream of changing inputs. Every time it receives a new piece of text, it resets its timer. It will only output the very last piece of text it received, and only after the inputs have stopped changing for the specified number of seconds. It’s perfect for situations where you have a rapid series of updates (like from a text box you are typing in) and you only want the final, settled result to be processed.

In short:

Use Delay Node when you need to say, "Wait 5 seconds, then do the next thing."

Use Dynamic Delay Text when you need to say, "Wait until things have been quiet for 5 seconds, then use the last thing I gave you."

<img width="563" height="224" alt="image" src="https://github.com/user-attachments/assets/9d3e78ba-50f3-49e5-ad84-a2baeb27df54" />





Collect And Distribute Text: A critical logic node for managing and synchronizing text streams from multiple sources.

IMGToIMGConditioning: A smart utility that bundles several steps into one logical block for img2img workflows.

Dynamic Start Index: A logic tool for controlling batch processing by dynamically setting the starting point.

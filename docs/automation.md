## ⚙️ Conditional LoRA Applier
An intelligent node that automatically applies the correct LoRAs to your model and CLIP based on keywords found in your prompt.

Philosophy & Use Case: The Conditional LoRA Applier is your automated workflow director. Its purpose is to eliminate the need for complex switches or manually changing LoRAs every time you change your prompt. You create a simple "rulebook" that tells the node, "If you see the word 'portrait' in the prompt, apply my favorite portrait LoRA." This allows you to build universal, "set-it-and-forget-it" workflows that intelligently adapt to your creative ideas. It can apply multiple LoRAs if multiple rules are met, and even apply a default "house style" LoRA if no other rules match.

General Usage: The node takes your main model and clip as inputs. Its logic is controlled by two main text boxes:

prompt: This is where you connect the text prompt you intend to use for generation. The node reads this text to look for your keywords.

lora_definitions: This is your "rulebook." You define your rules here, one per line, using a simple format. The node includes helpful comments explaining exactly how to write them. The basic format is:

keyword1, keyword2 : path/to/your/lora.safetensors, model_strength, clip_strength

Default LoRA: You can use the dropdowns to select a default_lora_name that will be applied automatically only if no keywords from your rulebook are found in the prompt. This is perfect for setting a general style.

<img width="1338" height="673" alt="image" src="https://github.com/user-attachments/assets/50bc9c02-5c9a-446f-b465-d90a9b1f4937" />

### ⚙️ Chain Workflow (API)

A utility node that allows you to automatically trigger a secondary workflow via the ComfyUI API once the current workflow finishes.

<img width="312" height="101" alt="image" src="https://github.com/user-attachments/assets/01ac2173-ec51-4a52-85e0-2731551451ff" />


**Philosophy & Use Case:**  
This node acts as a "relay baton" for your generative pipeline. It is designed to solve the **VRAM Bottleneck** that occurs when trying to run multiple massive models (e.g., Flux for image generation + WAN for video generation) in a single workspace.

By splitting your process into two separate files and using this node to bridge them, you ensure that the first workflow completely unloads its models and frees its VRAM before the second workflow begins. It allows for "Infinite Chaining" of workflows without the resource cost of a monolithic graph.

**General Usage:**  
The node sends a command to your local ComfyUI server to queue a specific `.json` file.

*   **trigger_image:** Connect the output of your `Save Image` node here. This input is not used for image processing, but to **force execution order**. It ensures the new workflow is only queued *after* the image has been successfully saved to disk.
*   **json_path:** The full local path to the workflow file you want to run next.

> [!IMPORTANT]  
> **CRITICAL REQUIREMENT:**  
> The target workflow file must be saved using the **"Save (API Format)"** button in your ComfyUI settings (enabled via Dev Mode options). If you try to load a standard workflow JSON, the server will reject the command.
> 


<img width="3500" height="2500" alt="Namnlös" src="https://github.com/user-attachments/assets/e46fd2e9-f1bf-4a09-b62f-cd671b69e700" />


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

## ⚙️ Collect and Distribute Text
A utility node for gathering multiple text inputs over time and outputting them as a single, combined block.

Philosophy & Use Case: This node acts as a "text accumulator" or a synchronization point in your workflow. It's designed for complex scenarios where you have multiple, separate processes generating text (like a loop analyzing a batch of images one by one) and you need to gather all those individual pieces of text into a single, coherent document before passing it to the next stage. It ensures that your final processing node (like a summarizer) gets the complete story, not just one chapter at a time.

General Usage: The node accumulates any text it receives at its text input. It has two modes for outputting the final combined text:

Timed Output: If the trigger is False, the node waits for a pause in the incoming text stream. Every time new text arrives, it resets a timer. When the timer (defined by seconds) finally runs out, it outputs everything it has collected.

Manual Trigger: If you set the trigger input to True, the node will immediately output all the text it has accumulated up to that point and reset itself. This gives you precise manual control over the release of the data.

<img width="416" height="197" alt="image" src="https://github.com/user-attachments/assets/f2e61349-ec14-45c0-bd2c-b82f49e300a9" />




## ⚙️ IMG To IMG Conditioning
A utility node that simplifies img2img workflows by encoding an image and applying its data to the positive and negative conditioning streams in a single step.

Philosophy & Use Case: This node is a workflow accelerator specifically for img2img tasks. Normally, you would need to encode your source image into a latent and then use other nodes to apply that latent to your conditioning. This node bundles that entire process into one clean operation. It takes your source image, encodes it, and injects that visual information directly into your positive and negative prompts, preparing them for the KSampler.

General Usage: You connect your standard positive and negative conditioning, your VAE, and the source image you want to use as a base. The node then outputs the modified positive and negative conditioning streams, which now contain the encoded image data, along with a blank latent ready for the sampling process. It's a clean and efficient way to set up an img2img pipeline.

<img width="344" height="132" alt="image" src="https://github.com/user-attachments/assets/3cf9638f-0fe9-44a1-a22b-2d3dfa46b065" />


## ⚙️ Dynamic Start Index
A utility node that acts as a persistent counter, providing an incrementing index for batch processing and solving the "Batch Amnesia" problem in looped workflows.

Philosophy & Use Case: The Dynamic Start Index is the memory for your loops. In complex video or batch processing, you often need to process data in chunks (e.g., 30 frames at a time). This node keeps track of where the last batch ended and tells the next run where to begin. It solves "Batch Amnesia" by remembering "we finished at frame 60, so the next run must start at frame 61." The reset_counter toggle allows you to instantly reset the process back to the beginning without any rewiring.

General Usage: The node outputs an integer that you connect to the start_at_frame input of a batch loader node (like the VHS Load Video node).

batch_size: You set this to match the number of frames you are processing in each loop.

reset_counter: Toggling this will reset the counter back to zero on the next run.

The node will output 0 on the first run, 30 on the second, 60 on the third, and so on (assuming a batch size of 30), telling your loader exactly which chunk of frames to load next.

<img width="411" height="171" alt="image" src="https://github.com/user-attachments/assets/7e925e3b-e393-4e8f-8134-5abda7a63edf" />


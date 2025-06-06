# ComfyUI-Creepy_nodes
A collection of custom nodes for ComfyUI

A collection of switch nodes, dynamic nodes, evaluation nodes, translation node and some other specialized nodes.

### Installing

Search for "creepy nodes" in [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) and install.

Manual installation:

Open a command prompt from your /custom_nodes/ComfyUI-Creepy_nodes/ folder and type:  

`git clone https://github.com/Creepybits/ComfyUI-Creepy_nodes.git`

Then type: `..\..\python_embeded\python.exe -m pip install -r requirements.txt` 

Or `\full path to your python\python.exe -m pip install -r requirements.txt`


Restart ComfyUI  

___

### Free Beginner's Toolkit

The Free Beginner's Toolkit includes the following:
* 7 Essential Custom Nodes
* A 20+ pages detailed guide
* A versatile and useful workflow

It's available for download here: [Free Beginner's Toolkit](https://www.zanno.se/free-comfyui-beginner-toolkit/) 

![beginner ](https://github.com/user-attachments/assets/b5746ba9-2753-4e48-a9ff-1863fa3c6393)

___


### Save Images To Google Drive node pack
  
Save Images To Google Drive node pack includes:
* Custom Node for saving images directly to Google Drive from ComfyUI
* Detailed PDF guide on how to setup your own Google Drive API

The node and guide are available here: [Save Images To Google Drive](https://patreon.com/creepybits)

![image](https://github.com/user-attachments/assets/a58de484-7346-469a-b737-d3fc4812034e)

___

## ALL CREEPY NODES

![workflow (1)](https://github.com/user-attachments/assets/c829288d-9177-4c47-80e8-8ee5066a542c)


___


## GEMINI 2.5 FLASH/PRO API

![image](https://github.com/user-attachments/assets/ed555797-341c-4d3b-88e8-e48644fa425c)  

This node is experimental!

![image](https://github.com/user-attachments/assets/430ab812-5093-4de7-8edd-1ea6e4a23463)  

* Image: regular image input
* System prompt: Customize a system prompt (some models require that the system prompt and user instructions use the same input, if you get an error message try to use the same text input or without a system prompt)
* Model: Chose between the following models (note that the free API calls are much more limited for the 2.5 models)
* - gemini 2.5 flash preview
  - gemini 2.5 pro experimental
  - gemini 2.0 Flash
  - gemini 2.0 Flash Experimental
* max output tokens: (the 2.5 models require much higher output tokens than the 2.0 model)

  
* Temperature: Acts like a "creativity dial"
* - Higher Temperature: Makes the output more random, surprising, and potentially creative (but also riskier for coherence).
  - Lower Temperature: Makes the output more focused, deterministic, and predictable (sticking to more probable words).
* Top K: Limits the pool of possible next words to the K most likely options.
* - Higher K: More options considered, leading to more diverse text.
  - Lower K: Fewer options considered (only the very top ones), leading to more predictable text.
* Top P (Nucleus Sampling): Limits the pool of possible next words to the smallest set whose cumulative probability adds up to P.
* - Higher P: Includes a larger, more diverse set of words whose probabilities collectively reach the threshold. This adjusts dynamically based on how confident the model is.
  - Lower P: Restricts choices to a smaller set of highly probable words.
* User instructions: Write additional instructions.
* API key: Get your free API key here: [Gemini API](https://aistudio.google.com/apikey)
* - Save your key in a text file named `gemini_api_key.txt`, copy the path to the file and paste it in the text box for API.
* Resize image to: If you load a lot of images in a batch, resizing them to a smaller size can save time and tokens.
* Thinking mode: The 2.5 models have a "thinking mode" where you can follow their reasoning. Not very useful in Comfy, but you can use it if you want. You will have to explicity tell Gemini that the output should include the thinking (costs a lot more output tokens).

___  
## CONDITIONAL LORA LOADER  

![image](https://github.com/user-attachments/assets/9b2e72b5-3543-49d6-80f6-bd9aa9fecd1f)

This node will load loras based on if keywords (that you set) is present somewhere in the prompt.

* Format: keyword_phrase: lora_full_relative_path, lora_strength, clip_strength
* Example (use forward slashes for paths):
* portrait: Flux/Details/amateur_photo_v1.safetensors, 0.75, 1.0
* cinematic scene: MyLoRAs/Styles/retro_cinematic_v2.safetensors, 0.8, 0.9
* fantasy creature: Custom/Creatures/mythic_beast_lora.safetensors, 0.9, 0.9
* Use comma-separated values for strength. Default is 1.0 if omitted.
* Keep strength between -2.0 and 2.0.
* The keyword_phrase should be found anywhere in the prompt (case-insensitive by default).
* Use several keywords for each lora by separate them as:
   keyword_1, keyword_2: MyLoRAs/Styles/retro_cinematic_v2.safetensors, 0.8, 0.9
   This will load the lora _retro_cinematic_v2.safetensors_ from the path _MyLoRAs/Styles/_ if _keyword_1_ and/or _keyword_2_ is present anywhere in the prompt.   

___
## AUDIO NODES  

* Random/Fixed Audio Picker
* Audio To Image Draft
* Gemini Audio Analyzer 

![image](https://github.com/user-attachments/assets/e97ff31f-41f7-4cf3-80e4-93085a13e112)  

___  

**Random/Fixed Audio Picker**  
  
![image](https://github.com/user-attachments/assets/0de9f9ed-a6c0-4e8f-b325-74a81b75d7a9)  

> Segment Lengt:  
> Set how long the audio clip you forward to Gemini Audio Analyzer should be in seconds (max 600 seconds)  
>
> Start Time:  
> Set how far in your selected audio clip should begin, in seconds (or -1 to pick start time at random)
___
  
**Audio To Image Draft**  

![image](https://github.com/user-attachments/assets/917dfa5f-be83-4644-86fb-580faf91e2f4)  

> Will load a system prompt located at `\custom_nodes\ComfyUI_Creepy_Nodes\assets\prompts\audio_keywords.txt`
>
> If you have additional or special instructions regarding how and what adio should be analyzed, you can enter the instructions in the text box.

___

**Gemini Audio Analyzer**  

![image](https://github.com/user-attachments/assets/f23f7ebc-0e83-48a8-81c1-814a3ebfa3c6)  

A lot of the code for this node is inspired by, or borrowed from, [Gemini 2.0 Flash Exp](https://github.com/ShmuelRonen/ComfyUI-Gemini_Flash_2.0_Exp)  

> The API key will load automatically from `\custom_nodes\ComfyUI_Creepy_Nodes\assets\scripts\gemini_api_key.txt` if field is left empty.
> Pick between:
> * Gemini 2.0 Flash
> * Gemini 2.5 Pro
> * Gemini 2.5 Flash
___
    

## SWITCHES

![image](https://github.com/user-attachments/assets/1d4b9449-95ff-4afc-ade1-01c122ae8152)





* Multi Model Switch
* Multi VAE Switch
* Multi Clip Switch
* Multi Text Switch

These nodes works as you might expect them to. You can connect 3 different input nodes, and decide which to use by enter a number between 1-3 in the nodes.

* Dynamic Model Switch
* Dynamic Clip Switch
* Dynamic VAE switch
* Dynamic Conditioning switch
* Dynamic Latent Switch
* Dynamic Image Switch

These nodes works differently. The node will check input 1 and if there is a valid input in that slot it will forward it, if there is no input or an invalid input in the first input slot it will move on to the second one. If there's a valid input in the second slot it will use that one, else it will move to the third one. If no valid inputs are presented, the node will do nothing.

## DELAY NODES 

These nodes will delay the execution of the node following the delay node by x seconds.

![image](https://github.com/user-attachments/assets/11d43693-0ada-435b-aded-a7ffc0a42fff)


## SPECIAL NODES

* Sanitize Filename
* Evaluater Node
* People Evaluation Node
* Custom Node Manager
* Load Batch From Dir
* Keyword Extractor
* Summary Writer
* Prompt Generator
* Gemini Token Counter
* IMG To IMG Conditioning

### Sanitize Filename  
The _Sanitize Filename_ node will make sure that no invalid characters are forwarded to the _save image_ node.    
  
![image](https://github.com/user-attachments/assets/e0e55b39-efe2-460e-b25b-62c130680a30)  

___  

### Evaluater Node    
The _Evaluater Node_ fetches and forwards a system prompt to [Gemini 2.0 Flash Experimental](https://github.com/ShmuelRonen/ComfyUI-Gemini_Flash_2.0_Exp) node for evaluating and grading images.  

It will give a short answer with just a number between 1-10 when using _evaluate_img.txt_ 

![Skärmbild 2025-04-18 061747](https://github.com/user-attachments/assets/64f53f5f-8832-4003-9234-81f52c8241fe)  


It will give a longer explanation to the reasoning behind the grading when using _evaluate_img_long.txt_

![Skärmbild 2025-04-18 061809](https://github.com/user-attachments/assets/84606ff9-33a2-42fe-8553-ae703894f230)

___  

### People Evaluation Node
The _People Evaluation Node_ I made just for fun, and it will rate the attractiveness/sexiness of people in images. It currently has 4 settings:  

* attractiveness_nice
* attractiveness_rude
* attractiveness_x
* attractiveness_xx


_Attractiveness_nice_
  ![image](https://github.com/user-attachments/assets/72dc83dc-8503-4002-86c6-29c0452e9797)


_Attractiveness_rude_
 ![image](https://github.com/user-attachments/assets/893dbbfb-a299-49ea-a599-df8cad39b29d)

_Attractiveness_x_ 
![image](https://github.com/user-attachments/assets/10e327d6-2c43-4e46-968a-5b910491785c)

_Attractiveness_xx_
 ![image](https://github.com/user-attachments/assets/95f6d82e-0fba-4e2f-acfe-2b6d6dea1ca2)  

___  

### Custom Node Manager  
This node has two scan modes:
* Validate Python  

 ![image](https://github.com/user-attachments/assets/17c5c79f-f32e-44b3-9a31-9324b7f492df)

This will scan a directory for valid ComfyUI nodes. If a node is a valid ComfyUI node it will forward the information in the output.  

![image](https://github.com/user-attachments/assets/6126e9d8-bb31-4ab2-a466-66b647747cce)

* Check Libraries

![image](https://github.com/user-attachments/assets/6188f0e0-4e5a-4f7d-9902-b015dd0e4090)

This will scan a directory and gather information about imported libraries, and which nodes that imported them. The output will only list nodes that acrtually use import {module} (nodes that doesn't require a specific library will be skipped) look like this:

![image](https://github.com/user-attachments/assets/737cb55d-14f6-40a5-adb5-4e058a724a7a)

Any folder path can be set in the "directory" textbox. If left empty it will use `custom_nodes/creepy_nodes/assets/nodes` as its default root directory.  
___

### Load Batch From Dir  

![image](https://github.com/user-attachments/assets/c819daa2-31e3-422b-a56e-1d481ca7fc47)

A large part of the code for this node comes from [ComfyUI Inspire Pack](https://github.com/ltdrdata/ComfyUI-Inspire-Pack)

___

### Keyword Extractor

![image](https://github.com/user-attachments/assets/204efae9-6c7f-4db6-96af-ba6998461812)

This node will extract keywords from an image. In the textbox, describe which types of keywords it should extract.

___  

### Summary Writer

![image](https://github.com/user-attachments/assets/36425dea-6952-46e6-9929-03676fc9c49c)

Basically the same as Keyword Extractor, but lets you add several files in `/custom_nodes/creepy_nodes/assets/summary.json` to pick from in dropdown list.   

___

### Prompt Generator

![image](https://github.com/user-attachments/assets/52bb97db-d890-4d79-affb-1feeaa175f2c)

Basically the same as the System Prompt node.

___

### Gemini Token Counter

![image](https://github.com/user-attachments/assets/ecd443e4-d92e-4e6d-a6a2-00b8881cf161)

Estimates how many tokens your API call will cost  

___  

### IMG To IMG Conditioning  


![image](https://github.com/user-attachments/assets/12bd2e8e-0104-47be-9f81-2b7d24e1380f)  

Largely based of the official [InstructPixToPixConditioning](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy_extras/nodes_ip2p.py) node  



## ARGOS TRANSLATE NODE

![image](https://github.com/user-attachments/assets/5d1263dd-c92b-45ba-a08c-9d170d2fb35e)

This node is very much under development and is an attempt to incorporate the translate code for locally translating see: [Argos](https://github.com/argosopentech/argos-translate)  
Index over available languages are here: [Language index](https://www.argosopentech.com/argospm/index/)  

But from my experience it's easier to install language packages through [Argos GUI](https://github.com/argosopentech/argos-translate-gui) to be sure they install correctly.


_NOTE THIS NODE HAS A LOT OF WORK AHEAD AND WILL BE UPDATED SPORADICALLY_
    
___  

## SYSTEM PROMPT

![image](https://github.com/user-attachments/assets/92509bbc-3bd3-4409-b28b-81a227073782)

This node will automatically load a predetermined system prompt to the [Gemini 2.0 Experimental node](https://github.com/ShmuelRonen/ComfyUI-Gemini_Flash_2.0_Exp) and transform even short and inexact prompts to prompts that are suitable for Flux and Shuttle 3.1 together with the T5-XXL Clip. I created this node to make workflows a little bit less confusing, now there's no need to worry about the system prompt or wonder where to write the instructions to Gemini.

The current system prompt is written to work for both Text to image and image to image workflows. It's created to work with Gemini 2.0 Flash Experimental. It might work with other LLM's, but that's nothing I can guarantee. If you want to alter the actual system prompt, it is located in `/custom_nodes/creepy_nodes/assets/prompts/system_prompt.txt`

### EXAMPLE
![image](https://github.com/user-attachments/assets/e4746af1-55be-4363-b420-f271615ab7ac)

  ___  

  
### TESTS

I did some tests using 1 image and the same seed/setting, only changing the system prompt. The old system prompt I used was the following:
>You are an AI assistant specializing in crafting professional and efective prompts for the Flux model, suitable for the t5-xxl clip. You are specialized in creating prompts for generating realistic looking images based off another image. When an image or text is provided, you should generate a concise and descriptive prompt that will create a realistic looking image based of the traits of the image or text that is provided. The prompt should be between 150-300 tokens. The output should only show the final prompt, without any additional comments or instructions.
>

![USE OLD](https://github.com/user-attachments/assets/1f3daf13-7bb5-49b0-b624-f77e1a64c497)

And this is the Image to Image and Text to Image that are created with the _system prompt node_.


![systemnode](https://github.com/user-attachments/assets/154b1651-2d06-46ad-8221-a2ad91d0a4f7)




These nodes doesn't require any extra installations. You do however need to install [Gemini 2.0 Flash Experimental](https://github.com/ShmuelRonen/ComfyUI-Gemini_Flash_2.0_Exp) and set up the API in order to use the _system prompt node_. Alternatively, you can try it with another LLM, but I have no idea how, or even if, that would work.


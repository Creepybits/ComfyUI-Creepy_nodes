# ComfyUI-Creepy_nodes
A collection of switch nodes for ComfyUI

This set of nodes contains a set of easy switch nodes, and they don't require any extra installations. 

### Installing

Open a command prompt from your custom_nodes folder and type:  

`git clone https://github.com/Creepybits/ComfyUI-Creepy_nodes.git`

You can also install from [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager).

Restart ComfyUI

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

* Evaluater Node
* Sanitize Filename
* People Evaluation Node

The _Sanitize Filename_ node will make sure that no invalid characters are forwarded to the _save image_ node.  
  
The _Evaluater Node_ fetches and forwards a system prompt to [Gemini 2.0 Flash Experimental](https://github.com/ShmuelRonen/ComfyUI-Gemini_Flash_2.0_Exp) node for evaluating and grading images.  
  
The _People Evaluation Node_ I made just for fun, and it will rate the attractiveness/sexiness of people in images. It currently has 4 settings:  

* attractiveness_nice
* attractiveness_rude
* attractiveness_x
* attractiveness_xx

![image](https://github.com/user-attachments/assets/0bc774d9-2b5a-40f3-8915-88328740fe2e)

## Attractiveness_nice
  ![image](https://github.com/user-attachments/assets/72dc83dc-8503-4002-86c6-29c0452e9797)


## Attractiveness_rude
 ![image](https://github.com/user-attachments/assets/893dbbfb-a299-49ea-a599-df8cad39b29d)

 ## Attractiveness_x 
![image](https://github.com/user-attachments/assets/10e327d6-2c43-4e46-968a-5b910491785c)

 ## Attractiveness_xx
 ![image](https://github.com/user-attachments/assets/95f6d82e-0fba-4e2f-acfe-2b6d6dea1ca2)  

     

## ARGOS TRANSLATE NODE

![image](https://github.com/user-attachments/assets/5d1263dd-c92b-45ba-a08c-9d170d2fb35e)

This node is very much under development and is an attempt to incorporate the translate code for locally translating see: [Argos](https://github.com/argosopentech/argos-translate)  
Index over available languages are here: [Language index](https://www.argosopentech.com/argospm/index/)  

But from my experience it's easier to install language packages through [Argos GUI](https://github.com/argosopentech/argos-translate-gui) to be sure they install correctly.


_NOTE THIS NODE HAS A LOT OF WORK AHEAD AND WILL BE UPDATED SPORADICALLY_
    

## SYSTEM PROMPT

![image](https://github.com/user-attachments/assets/92509bbc-3bd3-4409-b28b-81a227073782)

This node will automatically load a predetermined system prompt to the [Gemini 2.0 Experimental node](https://github.com/ShmuelRonen/ComfyUI-Gemini_Flash_2.0_Exp) and transform even short and inexact prompts to prompts that are suitable for Flux and Shuttle 3.1 together with the T5-XXL Clip. I created this node to make workflows a little bit less confusing, now there's no need to worry about the system prompt or wonder where to write the instructions to Gemini.

The current system prompt is written to work for both Text to image and image to image workflows. It's created to work with Gemini 2.0 Flash Experimental. It might work with other LLM's, but that's nothing I can guarantee. If you want to alter the actual system prompt, it is located in `/custom_nodes/creepy_nodes/assets/prompts/system_prompt.txt`

### EXAMPLE
![image](https://github.com/user-attachments/assets/e4746af1-55be-4363-b420-f271615ab7ac)


### TESTS

I did some tests using 1 image and the same seed/setting, only changing the system prompt. The old system prompt I used was the following:
>You are an AI assistant specializing in crafting professional and efective prompts for the Flux model, suitable for the t5-xxl clip. You are specialized in creating prompts for generating realistic looking images based off another image. When an image or text is provided, you should generate a concise and descriptive prompt that will create a realistic looking image based of the traits of the image or text that is provided. The prompt should be between 150-300 tokens. The output should only show the final prompt, without any additional comments or instructions.
>

![USE OLD](https://github.com/user-attachments/assets/1f3daf13-7bb5-49b0-b624-f77e1a64c497)

And this is the Image to Image and Text to Image that are created with the _system prompt node_.


![systemnode](https://github.com/user-attachments/assets/154b1651-2d06-46ad-8221-a2ad91d0a4f7)




These nodes doesn't require any extra installations. You do however need to install [Gemini 2.0 Flash Experimental](https://github.com/ShmuelRonen/ComfyUI-Gemini_Flash_2.0_Exp) and set up the API in order to use the _system prompt node_. Alternatively, you can try it with another LLM, but I have no idea how, or even if, that would work.


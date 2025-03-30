# ComfyUI-Creepy_nodes
A collection of switch nodes for ComfyUI

This set of nodes contains a set of easy switch nodes, and they don't require any extra installations. 

### Installing

Open a command prompt from your custom_nodes folder and type:  

`git clone https://github.com/Creepybits/ComfyUI-Creepy_nodes.git`

You can also install from [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager).

Restart ComfyUI

## NODES

![image](https://github.com/user-attachments/assets/8ffac049-a897-40b2-be2b-a6c76d65cda5)



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

These nodes works differently. The node will check input 1 and if there is a valid input in that slot it will forward it, if there is no input or an invalid input in the first input slot it will move on to the second one. If there's a valid input in the second slot it will use that one, else it will move to the third one. If no valid inputs are presented, the node will do nothing.




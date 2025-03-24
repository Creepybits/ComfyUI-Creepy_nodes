# ComfyUI-Creepy_nodes
A collection of switch nodes for ComfyUI

This set of nodes contains a set of easy switch nodes, and they don't require any extra installations. 

### Installing

Open a command prompt from your custom_nodes folder and type:  

`git clone https://github.com/Creepybits/ComfyUI-Creepy_nodes.git`

I will also request the nodes to get included in [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) as soon as possible.

Restart ComfyUI

## NODES

![Skärmbild 2025-03-23 224928](https://github.com/user-attachments/assets/964bc9b5-dd14-4771-96fd-df7b0aa912a5)


* Multi Model Switch
* Multi VAE Switch
* Multi Clip Switch
* Multi Text Switch

These nodes works as you might expect them to. You can connect 3 different input nodes, and decide which to use by enter a number between 1-3 in the nodes.

* Dynamic Model Switch
* Dynamic Clip Switch

These two nodes works differently. The node will check input 1 and if there is a valid input in that slot it will forward it, if there is no input or an invalid input in the first input slot it will move on to the second one. If there's a valid input in the second slot it will use that one, else it will move to the third one. If no valid inputs are presented, the node will do nothing.

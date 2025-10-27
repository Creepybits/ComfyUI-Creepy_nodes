

Conditional LoRA Applier: The perfect example of workflow logic. It intelligently applies LoRAs based on keywords found in the prompt.

All Switch Nodes (Dynamic/Static): DynamicModelswitch, DynamicClipswitch, DynamicLatentSwitch, DynamicImageSwitch, DynamicVAESwitch, Textswitch, FallbackTextSwitch. These are the routers and decision-makers of your workflow.

All Delay Nodes: DelayNode, DelayTextNode, DynamicDelayText. These are the pacemakers, controlling the timing and sequence of operations.

Collect And Distribute Text: A critical logic node for managing and synchronizing text streams from multiple sources.

IMGToIMGConditioning: A smart utility that bundles several steps into one logical block for img2img workflows.

Dynamic Start Index: A logic tool for controlling batch processing by dynamically setting the starting point.

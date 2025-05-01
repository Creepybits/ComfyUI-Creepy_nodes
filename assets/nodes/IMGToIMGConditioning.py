# --- START OF FILE IMGToIMGConditioning.py ---

import torch

class IMGToIMGConditioning:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"positive": ("CONDITIONING", ),
                             "negative": ("CONDITIONING", ),
                             "vae": ("VAE", ),
                             "image": ("IMAGE", ),
                             }}

    RETURN_TYPES = ("CONDITIONING","CONDITIONING","LATENT")
    RETURN_NAMES = ("positive", "negative", "latent")
    FUNCTION = "encode"

    CATEGORY = "Creepybits/IMG2IMG"

    def encode(self, positive, negative, image, vae):

        # Calculate dimensions that are multiples of 8
        x = (image.shape[1] // 8) * 8
        y = (image.shape[2] // 8) * 8

        # Crop the image if its dimensions are not a multiple of 8
        if image.shape[1] != x or image.shape[2] != y:
            # Calculate offsets to center the crop
            x_offset = (image.shape[1] - x) // 2
            y_offset = (image.shape[2] - y) // 2
            image = image[:, x_offset : x + x_offset, y_offset : y + y_offset, :]


        # Encode the (potentially cropped) image into latent space using the VAE
        concat_latent = vae.encode(image)

        # Create the latent output for the node's third output
        # This is often a zero tensor matching the shape of the encoded image latent
        out_latent = {}
        out_latent["samples"] = torch.zeros_like(concat_latent)

        out = []
        # Process positive and negative conditioning lists
        for conditioning in [positive, negative]:
            c = []
            # Each item 't' in the conditioning list is typically a tuple (tensor, dictionary)
            for t in conditioning:
                # Get the tensor part (usually text embeddings)
                tensor_part = t[0]
                # Get the dictionary part and make a shallow copy to avoid modifying the original
                d = t[1].copy()

                # --- START OF THE FIX ---
                # Add the encoded latent image to the dictionary part
                # Explicitly detach and clone the tensor to create a new independent copy
                # This helps prevent issues with tensor history or caching across executions
                d["concat_latent_image"] = concat_latent.detach().clone()

                # Create the new conditioning item (original tensor + modified dictionary)
                n = [tensor_part, d]
                c.append(n)
            out.append(c)

        # Return the modified positive conditioning, negative conditioning, and the latent output
        # This tuple structure matches the RETURN_TYPES and RETURN_NAMES
        return (out[0], out[1], out_latent)

# ... rest of the file (NODE_CLASS_MAPPINGS, etc.) ...

NODE_CLASS_MAPPINGS = {
    "IMGToIMGConditioning": IMGToIMGConditioning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "IMGToIMGConditioning": "IMG To IMG Conditioning (Creepybits)",
}

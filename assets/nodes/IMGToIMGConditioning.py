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

        
        x = (image.shape[1] // 8) * 8
        y = (image.shape[2] // 8) * 8

        
        if image.shape[1] != x or image.shape[2] != y:
            x_offset = (image.shape[1] - x) // 2
            y_offset = (image.shape[2] - y) // 2
            image = image[:, x_offset : x + x_offset, y_offset : y + y_offset, :]


        concat_latent = vae.encode(image)

        out_latent = {}
        out_latent["samples"] = torch.zeros_like(concat_latent)

        out = []        
        for conditioning in [positive, negative]:
            c = []            
            for t in conditioning:                
                tensor_part = t[0]                
                d = t[1].copy()

                d["concat_latent_image"] = concat_latent.detach().clone()
                
                n = [tensor_part, d]
                c.append(n)
            out.append(c)

        return (out[0], out[1], out_latent)


NODE_CLASS_MAPPINGS = {
    "IMGToIMGConditioning": IMGToIMGConditioning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
      "IMGToIMGConditioning": "IMG To IMG Conditioning (Creepybits)",
}

import os
from huggingface_hub import InferenceClient

class ImageGeneration:
    def __init__(self):
        self.client = InferenceClient(
        provider="nscale",
        api_key=os.environ["HF_TOKEN"],
    )
        
    async def generateImage(self,prompt:str):
        image = self.client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0",
        )
        return image

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, DDIMScheduler, DPMSolverSDEScheduler, EulerAncestralDiscreteScheduler
import warnings





def generate_image(prompt):
    pipe = StableDiffusionPipeline.from_single_file(
        "C:\sdwebui\Stable2\stable-diffusion-webui\models\Stable-diffusion\epicrealism_pureEvolutionV3.safetensors",
        torch_dtype=torch.float16,

    ).to("cuda")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    pipe.safety_checker = None
    with autocast("cuda"):
        image = pipe(prompt , num_inference_steps=25, guidance_scale=2.5, negative_prompt="lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature")["images"]
        image = image[0]
    print(prompt)
    file_name:str = prompt.replace(" ", "_")[:40]
    print(file_name)
    image.save("text2image/" + file_name + ".png")
    return "C:/Users/lukac/SIA/text2image/" + file_name + ".png"



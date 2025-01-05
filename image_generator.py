import time, os, asyncio

from diffusers import AutoPipelineForText2Image, DPMSolverMultistepScheduler, DiffusionPipeline
from PIL.Image import Image
from typing import overload, Tuple

import torch
import logging
logger = logging.getLogger()

# Float32 takes twice as much memory as float16, but is required due to a bug/issues specifically with NVIDIA GeForce GTX 1660 SUPER.
# This config may look different for different GPUs.
pipe = AutoPipelineForText2Image.from_pretrained('lykon/dreamshaper-xl-lightning', torch_dtype=torch.float32)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
# Options to consider for performance:
pipe.enable_sequential_cpu_offload()
pipe.enable_xformers_memory_efficient_attention()
# pipe.enable_model_cpu_offload()
# pipe.enable_vae_slicing()
# pipe.enable_vae_tiling()

# Optionally set seed for reproducibility, also needs to be uncommented below in the pipe
# generator = torch.manual_seed(42)

def generate_sync(prompts: list[str], negative_prompts: list[str]) -> Tuple[list[Image], list[str]]:
    images: list[Image] = pipe(
        prompt=prompts, 
        negative_prompt=negative_prompts, 
        num_inference_steps=7, # 7 is best, more is slower
        guidance_scale=2, # Recommended by model author
        # generator=generator,
        height=1024, # 1024 is best performance on this model. 512 is faster but lower quality and some models are not trained for it.
        width=1024
    ).images
    logger.info(images)
   
    # Define the directory and ensure it exists
    output_dir = 'worksheet/images'
    os.makedirs(output_dir, exist_ok=True)

    # Save the file in /images
    file_paths: list[str] = []
    for image in images:
        # convert image to black and white
        threshold = 100
        fn = lambda x : 255 if x > threshold else 0
        image = image.convert('L').point(fn, mode='1')
        
        timestamp = str(time.time())
        file_name = f"{timestamp}.png"
        file_path = os.path.join(output_dir, file_name)
        image.save(file_path)
        logger.info('Image saved to: %s', file_path)
        file_paths.append(file_path)

    return images, file_paths

  
# Add an async generate function that uses run_in_executor
async def generate(prompts: list[str], negative_prompts: list[str]):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, generate_sync, prompts, negative_prompts)


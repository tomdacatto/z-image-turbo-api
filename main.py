from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
# Lazy import diffusers - imported in load_model() to avoid import errors
from PIL import Image
import base64
import io
import os
from typing import Optional
import uvicorn

app = FastAPI(title="Z-Image-Turbo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_ID = "Tongyi-MAI/Z-Image-Turbo"
pipe = None

def load_model():
    global pipe
    from diffusers import DiffusionPipeline
    if pipe is None:
        pipe = DiffusionPipeline.from_pretrained(
                        MODEL_ID,
            torch_dtype=torch.bfloat16,
            variant="fp16"
        )
        pipe = pipe.to("cpu")
    return pipe

def image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

@app.on_event("startup")
async def startup_event():
    pass
@app.get("/health")
async def health():
    return {"status": "online", "model": MODEL_ID}

@app.post("/generate/text2img")
async def text_to_image(
    prompt: str = Form(...),
    height: int = Form(default=768),
    width: int = Form(default=768),
    steps: int = Form(default=4),
    guidance_scale: float = Form(default=0.0),
    seed: Optional[int] = Form(default=None),
    num_images: int = Form(default=1)
):
    try:
        pipe = load_model()
        
        if seed:
            generator = torch.Generator("cpu").manual_seed(seed)
        else:
            generator = None
        
        images = pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            num_images_per_prompt=num_images,
            generator=generator
        ).images
        
        result = {
            "images": [
                {
                    "base64": image_to_base64(img),
                    "format": "PNG"
                }
                for img in images
            ],
            "prompt": prompt,
            "height": height,
            "width": width,
            "steps": steps
        }
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/generate/img2img")
async def image_to_image(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    strength: float = Form(default=0.8),
    steps: int = Form(default=4),
    guidance_scale: float = Form(default=0.0),
    seed: Optional[int] = Form(default=None),
):
    try:
        pipe = load_model()
        
        img_data = await image.read()
        pil_image = Image.open(io.BytesIO(img_data)).convert("RGB")
        
        if seed:
            generator = torch.Generator("cpu").manual_seed(seed)
        else:
            generator = None
        
        output = pipe(
            prompt=prompt,
            image=pil_image,
            strength=strength,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator
        ).images[0]
        
        result = {
            "images": [
                {
                    "base64": image_to_base64(output),
                    "format": "PNG"
                }
            ],
            "prompt": prompt,
            "strength": strength,
            "steps": steps
        }
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, timeout_keep_alive=120)

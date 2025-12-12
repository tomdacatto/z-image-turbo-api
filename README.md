# Z-Image-Turbo API

A FastAPI endpoint for text-to-image and image-to-image generation using the Z-Image-Turbo model (Tongyi-MAI).

## Features

- Text-to-Image generation
- Image-to-Image transformation
- Base64 image encoding in responses
- CORS enabled for web integration
- Deployed on Railway

## API Endpoints

### Text-to-Image
`POST /generate/text2img`

**Parameters:**
- `prompt` (required): Text description for image generation
- `height` (default: 768): Image height
- `width` (default: 768): Image width
- `steps` (default: 4): Number of inference steps (1-8)
- `guidance_scale` (default: 0.0): Guidance scale for generation
- `seed` (optional): Random seed for reproducibility
- `num_images` (default: 1): Number of images to generate

### Image-to-Image
`POST /generate/img2img`

**Parameters:**
- `prompt` (required): Text description for transformation
- `image` (required): Reference image file (multipart/form-data)
- `strength` (default: 0.8): How much to transform the image (0-1)
- `steps` (default: 4): Number of inference steps
- `guidance_scale` (default: 0.0): Guidance scale
- `seed` (optional): Random seed

## Response Format

```json
{
  "images": [
    {
      "base64": "iVBORw0KGgoAAAANS...",
      "format": "PNG"
    }
  ],
  "prompt": "Your prompt here",
  "height": 768,
  "width": 768,
  "steps": 4
}
```

## Deployment

Deployed on Railway. The API is accessible at the Railway-provided URL.

## Technologies

- FastAPI
- PyTorch
- Diffusers (Hugging Face)
- Pillow
- Uvicorn

from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Z-Image-Turbo API", version="1.0.0")

@app.get("/health")
async def health():
    return {"status": "online", "message": "API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to Z-Image-Turbo API"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

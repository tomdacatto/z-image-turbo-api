from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import os
import base64

app = FastAPI(title="Z-Image-Turbo API", version="1.0.0")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Z-Image Turbo - AI Image Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 50px;
            animation: slideInUp 0.6s ease-out;
        }
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .form-group {
            margin-bottom: 25px;
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #333;
            font-weight: 600;
            font-size: 1.05em;
        }
        textarea, input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s ease;
            font-family: inherit;
        }
        textarea:focus, input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        button {
            flex: 1;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .btn-generate {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            flex: 2;
        }
        .btn-generate:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        .btn-generate:active:not(:disabled) {
            transform: translateY(0);
        }
        .btn-generate:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .btn-clear {
            background: #f0f0f0;
            color: #333;
        }
        .btn-clear:hover {
            background: #e0e0e0;
        }
        .result-container {
            margin-top: 40px;
            text-align: center;
            display: none;
            animation: slideInUp 0.5s ease-out;
        }
        .result-container.show {
            display: block;
        }
        .generated-image {
            max-width: 100%;
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
            margin: 20px 0;
            animation: zoomIn 0.6s ease-out;
        }
        @keyframes zoomIn {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        .loading {
            display: none;
            text-align: center;
            margin: 30px 0;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .status-message {
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
            animation: slideInUp 0.3s ease-out;
        }
        .status-message.show {
            display: block;
        }
        .status-message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status-message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status-message.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Z-Image Turbo</h1>
        <p class="subtitle">🎨 Free AI Image Generation</p>
        <form id="generateForm">
            <div class="form-group">
                <label for="prompt">Describe Your Image</label>
                <textarea id="prompt" placeholder="e.g., A futuristic city with neon lights at night..." required></textarea>
            </div>
            <div class="button-group">
                <button type="submit" class="btn-generate" id="generateBtn">✨ Generate Image</button>
                <button type="button" class="btn-clear" onclick="document.getElementById('prompt').value=''">Clear</button>
            </div>
        </form>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Generating your amazing image...</p>
        </div>
        <div id="statusMessage" class="status-message"></div>
        <div class="result-container" id="resultContainer">
            <h2>Your Generated Image</h2>
            <img id="resultImage" class="generated-image" alt="Generated Image" />
        </div>
        <div class="footer">
            <p>Powered by <strong>Z-Image Turbo API</strong></p>
            <p>Free & Fast Image Generation</p>
        </div>
    </div>
    <script>
        const form = document.getElementById('generateForm');
        const promptInput = document.getElementById('prompt');
        const generateBtn = document.getElementById('generateBtn');
        const loading = document.getElementById('loading');
        const statusMessage = document.getElementById('statusMessage');
        const resultContainer = document.getElementById('resultContainer');
        const resultImage = document.getElementById('resultImage');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const prompt = promptInput.value.trim();
            if (!prompt) {
                showStatus('Please enter a description for your image', 'error');
                return;
            }
            generateBtn.disabled = true;
            loading.classList.add('show');
            statusMessage.classList.remove('show');
            resultContainer.classList.remove('show');
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt }),
                });
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                const data = await response.json();
                if (data.image) {
                    resultImage.src = 'data:image/png;base64,' + data.image;
                    resultContainer.classList.add('show');
                    showStatus('✨ Image generated successfully!', 'success');
                } else {
                    throw new Error('No image data received');
                }
            } catch (error) {
                console.error('Error:', error);
                showStatus('Failed to generate image. Please try again.', 'error');
            } finally {
                loading.classList.remove('show');
                generateBtn.disabled = false;
            }
        });

        function showStatus(message, type) {
            statusMessage.textContent = message;
            statusMessage.className = `status-message show ${type}`;
            if (type === 'success') {
                setTimeout(() => {
                    statusMessage.classList.remove('show');
                }, 4000);
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return HTML_CONTENT

@app.post("/api/generate")
async def generate_image(request: dict):
    prompt = request.get("prompt", "")
    if not prompt:
        return {"error": "Prompt is required"}
    
    # Placeholder - returns a simple demo response
    # In production, this would use actual AI model
    return {
        "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
        "prompt": prompt,
        "message": "Demo image (placeholder)"
    }

@app.get("/health")
async def health():
    return {"status": "online", "message": "API is running"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "service": "z-image-turbo"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

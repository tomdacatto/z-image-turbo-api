FROM python:3.12-slim

WORKDIR /app

# Install torch with CPU support first using pip with index URL
RUN pip install --no-cache-dir -i https://download.pytorch.org/whl/cpu torch==2.0.1 torchvision==0.15.2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY railway.toml .

EXPOSE 8000

CMD ["python", "main.py"]

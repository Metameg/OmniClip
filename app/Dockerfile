FROM python:3.9-slim

# Install system dependencies required for Python, Rust, and ffmpeg
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    ffmpeg \
    libopenblas-dev \
    liblapack-dev \
    rustc \
    cargo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY requirements.txt ./

COPY . /app/

RUN pip install --upgrade pip && \ 
pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:8080 app.app:app
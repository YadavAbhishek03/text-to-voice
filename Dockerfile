FROM python:3.9-slim

WORKDIR /app

# Avoid tzdata prompts & update apt properly
ENV DEBIAN_FRONTEND=noninteractive

# Install ffmpeg and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]


FROM python:3.9-slim

WORKDIR /app

# Install ffmpeg and some basics
RUN apt-get update && apt-get install -y ffmpeg gcc python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Debug: Show installed packages
RUN pip list

CMD ["python", "app.py"]


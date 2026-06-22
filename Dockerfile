FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# These are often required by some OpenCV or machine learning libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# We use no-cache-dir to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD uvicorn backend_api:app --host 0.0.0.0 --port ${PORT:-8000}

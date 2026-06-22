FROM python:3.11-slim

# Create a non-root user (Required for Hugging Face Spaces)
RUN useradd -m -u 1000 user

# Set environment variables for the user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PORT=7860

# Set working directory to the user's home folder
WORKDIR $HOME/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the files to the non-root user
RUN chown -R user:user $HOME/app

# Switch to the non-root user
USER user

EXPOSE 7860

# Run the FastAPI application on port 7860
CMD ["uvicorn", "backend_api:app", "--host", "0.0.0.0", "--port", "7860"]

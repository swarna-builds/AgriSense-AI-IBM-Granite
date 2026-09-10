# Use lightweight official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first for Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Expose standard Streamlit port
EXPOSE 8080

# Configure Streamlit to run on container launch
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
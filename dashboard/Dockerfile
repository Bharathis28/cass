# CASS-Lite v2 Dashboard - Cloud Run Dockerfile
# Python 3.11 base image for optimal performance

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard files
COPY . .

# Expose port 8080 (Cloud Run standard)
EXPOSE 8080

# Run Streamlit on Cloud Run
CMD streamlit run app.py \
    --server.port=8080 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false

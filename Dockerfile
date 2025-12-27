FROM python:3.12-slim

# -------------------------------
# Install system dependencies
# -------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-eng \
        libtesseract-dev \
        pkg-config \
        python3-opencv \
        && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Create app directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Copy project files
# -------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_emails_phones.py .

# -------------------------------
# Start the script
# -------------------------------
CMD ["python3", "extract_emails_phones.py"]


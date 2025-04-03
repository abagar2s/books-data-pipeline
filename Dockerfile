# Use a slim and secure base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy full etl folder (for modular code, if needed)
COPY etl/ ./etl/
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Optionally create a volume (for local CSV/debugging)
VOLUME ["/app/data"]

# Default run command
CMD ["python", "etl/ingest.py"]

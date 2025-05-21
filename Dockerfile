# Use a stable slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Environment: avoid buffering issues
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose metrics port
EXPOSE 8000

# Run the service
CMD ["python", "app.py"]

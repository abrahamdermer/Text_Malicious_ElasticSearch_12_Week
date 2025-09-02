# This Dockerfile sets up a prodict server with FastAPI and Uvicorn

# Start from Python 3.13.2
FROM python:3.13.2

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Start the prodict server
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8080"]

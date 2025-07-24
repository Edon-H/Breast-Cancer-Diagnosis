# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory in docker container
WORKDIR /app

# Copy the FastAPI application files into the container
COPY main.py .
COPY model/ ./model/
COPY requirements.txt .

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Cloud Run's required port
EXPOSE 8080

# Command to start FastAPI using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

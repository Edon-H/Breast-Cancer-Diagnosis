# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy entire app directory including model
COPY app ./app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Cloud Run required port
EXPOSE 8080

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

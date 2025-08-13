# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the requirements file if exists and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app.py .

# Expose port 3345
EXPOSE 3345

# Run the app
CMD ["python", "app.py"]

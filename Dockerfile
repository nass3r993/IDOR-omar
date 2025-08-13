# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code, templates, and static files
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Expose port 3345
EXPOSE 3345

# Run the app
CMD ["python", "app.py"]

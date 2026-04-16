# Use an official Python runtime as a parent image.
# This image already includes Python 3.11 and a minimal Linux filesystem.
FROM python:3.11-slim

# Set the working directory inside the container.
# This folder is created automatically if it does not already exist.
WORKDIR /app

# Copy only the requirements file into the container first.
# This enables Docker to cache dependency installation separately from app code.
COPY requirements.txt .

# Install Python dependencies from requirements.txt.
# The installed packages become part of the image filesystem.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code into the container.
# Since WORKDIR is /app, this copies files into /app.
COPY . .

# Declare that the container listens on port 8000.
EXPOSE 8000

# Define the command that runs when the container starts.
# This launches Uvicorn and serves the FastAPI app from app.py.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y python3-dev gcc && \
    pip3 install RPi.GPIO && \
    pip install --no-cache-dir -r requirements.txt

# Run soil_sensing_service.py when the container launches
CMD ["python", "-u", "soil_sensing_service.py"]

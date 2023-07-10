# Start with a base image containing Python runtime
FROM python:3.9-slim-buster

# The maintainer name
LABEL maintainer="NickHarrisGit"

# Set the working directory in the container to /app
WORKDIR /app

# Copy the 'requirements.txt' from your local directory to the present working directory in your docker container
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y python3-dev gcc && \
    pip3 install RPi.GPIO && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app 
COPY . /app

# Run your python script when the container launches
CMD ["python", "-u", "day_night_led_service.py"]
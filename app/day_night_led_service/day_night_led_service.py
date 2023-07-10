import RPi.GPIO as GPIO
import time
import datetime
import paho.mqtt.client as mqtt

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
led_pin = 18  # Change to the pin you have the LED connected to
GPIO.setup(led_pin, GPIO.OUT)

# Initialize MQTT client
client = mqtt.Client()
client.connect("mqtt_broker", 1883, 60)

# Day and night hours
day_start = datetime.time(6, 0)
night_start = datetime.time(17, 0)

while True:
    # Get current time
    now = datetime.datetime.now().time()

    if day_start <= now < night_start:
        # Day time: turn on LED
        GPIO.output(led_pin, GPIO.HIGH)
        client.publish("gardenpi/day_night_status", "day")
    else:
        # Night time: turn off LED
        GPIO.output(led_pin, GPIO.LOW)
        client.publish("gardenpi/day_night_status", "night")

    time.sleep(60)  # Delay for 1 minute

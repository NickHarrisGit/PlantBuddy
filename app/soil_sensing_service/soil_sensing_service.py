import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
sensor_pin = 4
GPIO.setup(sensor_pin, GPIO.IN)

# Initialize MQTT client
client = mqtt.Client()
client.connect("mqtt_broker", 1883, 60)

# Calibration values
voltage_min = 0  # Voltage reading for dry soil
voltage_max = 1023  # Voltage reading for wet soil

while True:
    # Read data from sensor
    voltage = GPIO.input(sensor_pin)
    
    # Convert voltage to moisture percentage
    moisture = 100 * (voltage - voltage_min) / (voltage_max - voltage_min)
    
    # Publish moisture data
    client.publish("gardenpi/moisture", moisture)
    
    time.sleep(60)  # Delay for 1 minute

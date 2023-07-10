import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Define the pin that will be used for the LED strip
LED_PIN = 18

# Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize MQTT client
client = mqtt.Client()
client.connect("mqtt_broker", 1883, 60)

# Moisture threshold
moisture_threshold = 30

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("gardenpi/moisture")

def on_message(client, userdata, msg):
    # Convert message payload to moisture percentage
    moisture = float(msg.payload)

    if moisture < moisture_threshold:
        # Low moisture: turn on LED and send alert
        GPIO.output(LED_PIN, GPIO.HIGH)
        client.publish("gardenpi/led_alerts", "low_moisture")
    else:
        # Adequate moisture: turn off LED
        GPIO.output(LED_PIN, GPIO.LOW)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

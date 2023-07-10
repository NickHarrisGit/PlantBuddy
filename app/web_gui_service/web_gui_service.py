from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import requests
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/moisture')
def get_moisture():
    response = requests.get('http://data_persistence_service:5000/moisture')
    return jsonify(response.json())

@app.route('/led_alerts')
def get_led_alerts():
    response = requests.get('http://data_persistence_service:5000/led_alerts')
    return jsonify(response.json())

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("gardenpi/moisture")
    client.subscribe("gardenpi/led_alerts")

def on_message(client, userdata, msg):
    if msg.topic == "gardenpi/moisture":
        socketio.emit('moisture', msg.payload)
    elif msg.topic == "gardenpi/led_alerts":
        socketio.emit('led_alert', msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker with a connection loop
while True:
    try:
        client.connect('mqtt_broker', 1883, 60)
        print('Successfully connected to MQTT broker')
        break  # Connected, break the loop
    except:
        print('Failed to connect to MQTT broker, retrying...')
        time.sleep(3)  # Wait before retrying

if __name__ == '__main__':
    client.loop_start()
    socketio.run(app, host='0.0.0.0', port=8000)

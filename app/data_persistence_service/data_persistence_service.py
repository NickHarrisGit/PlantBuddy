import sqlite3
from sqlite3 import Error
import paho.mqtt.client as mqtt
import datetime
import time

# Database handling functions

DATABASE = 'db.sqlite3'

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(DATABASE)
        if conn is not None:
            create_tables(conn)
    except Error as e:
        print(e)

    return conn

def create_tables(conn):
    sql_create_moisture_readings_table = """CREATE TABLE IF NOT EXISTS moisture_readings (
                                                id integer PRIMARY KEY,
                                                timestamp text NOT NULL,
                                                reading text NOT NULL
                                            ); """
                                            
    sql_create_led_alerts_table = """CREATE TABLE IF NOT EXISTS led_alerts (
                                        id integer PRIMARY KEY,
                                        timestamp text NOT NULL,
                                        alert text NOT NULL
                                    ); """

    try:
        c = conn.cursor()
        c.execute(sql_create_moisture_readings_table)
        c.execute(sql_create_led_alerts_table)
    except Error as e:
        print(e)

# MQTT callback functions

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('gardenpi/moisture')
        client.subscribe('gardenpi/led_alerts')
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    conn = create_connection()
    cursor = conn.cursor()

    if msg.topic == 'gardenpi/moisture':
        insert_data_sql = ''' INSERT INTO moisture_readings(time, reading) VALUES(?, ?) '''
        cursor.execute(insert_data_sql, (datetime.datetime.now(), msg.payload))
    elif msg.topic == 'gardenpi/led_alerts':
        insert_data_sql = ''' INSERT INTO led_alerts(time, alert) VALUES(?, ?) '''
        cursor.execute(insert_data_sql, (datetime.datetime.now(), msg.payload))

    conn.commit()
    print('Record inserted successfully')
    conn.close()

# Set up MQTT client

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker with a connection loop
while True:
    try:
        client.connect('mqtt_broker', 1883, 60)
        break  # Connected, break the loop
    except:
        print('Failed to connect to MQTT broker, retrying...')
        time.sleep(3)  # Wait before retrying

# Run MQTT client loop

client.loop_start()
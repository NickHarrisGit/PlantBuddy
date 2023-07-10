import sqlite3
from sqlite3 import Error
import paho.mqtt.client as mqtt
import datetime

# Database handling functions

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('/path/to/your/database.db')
        return conn
    except Error as e:
        print(e)

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data(conn, insert_data_sql, data):
    try:
        cur = conn.cursor()
        cur.execute(insert_data_sql, data)
        return cur.lastrowid
    except Error as e:
        print(e)

# MQTT callback functions

def on_connect(client, userdata, flags, rc):
    print(f'Connected to MQTT broker with code {rc}')
    client.subscribe('gardenpi/moisture')
    client.subscribe('gardenpi/led_alerts')

def on_message(client, userdata, msg):
    conn = create_connection()
    cursor = conn.cursor()

    if msg.topic == 'gardenpi/moisture':
        insert_data_sql = ''' INSERT INTO moisture(time, moisture_value) VALUES(?, ?) '''
        cursor.execute(insert_data_sql, (datetime.datetime.now(), msg.payload))
    elif msg.topic == 'gardenpi/led_alerts':
        insert_data_sql = ''' INSERT INTO led_alerts(time, alert) VALUES(?, ?) '''
        cursor.execute(insert_data_sql, (datetime.datetime.now(), msg.payload))

    conn.commit()
    print('Record inserted successfully')

# Set up MQTT client

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)  # replace 'localhost' with the hostname of your MQTT broker

# Run MQTT client loop

client.loop_start()

# Database setup

sql_create_moisture_table = ''' CREATE TABLE IF NOT EXISTS moisture (
                                id integer PRIMARY KEY,
                                time text NOT NULL,
                                moisture_value real NOT NULL
                            ); '''

sql_create_led_alerts_table = ''' CREATE TABLE IF NOT EXISTS led_alerts (
                                  id integer PRIMARY KEY,
                                  time text NOT NULL,
                                  alert text NOT NULL
                              ); '''

conn = create_connection()

# create tables
if conn is not None:
    create_table(conn, sql_create_moisture_table)
    create_table(conn, sql_create_led_alerts_table)
else:
    print('Error: Cannot create the database connection.')

conn.close()

import paho.mqtt.client as mqtt # pip install paho.mqtt
import time
import numpy as np
import datetime


client = mqtt.Client()


broker_address = "test.mosquitto.org"
port = 1883

client.connect(broker_address, port, 60)

topic = "teds22/group9/pressure"
client.subscribe(topic)
client.loop_start()
for i in range(10):
    mu, sigma = 1200.00, 1.0
    reading = f'{round(np.random.normal(mu, sigma), 2):.2f}'        
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    message = f'{reading}|{dt}'
   
    client.publish(topic, message,qos=2)
    time.sleep(1)

time.sleep(4)
client.loop_stop()
client.disconnect()


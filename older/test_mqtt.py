from network_setup import Networker
from umqtt.simple import MQTTClient
import random
import time
import json

print("imports")
wlan = Networker().establish_connection()
print("wifi connection established")
client = MQTTClient('sense_board_1', '192.168.1.14', port=1883, keepalive=5)
print("mqtt broker connection established")

msg_num = 0

topic = b'test'
message_text = "Hello Raspberry"

def generate_message(k, v):
    return json.dumps({k : v})#.encode()

#message = json.dumps({msg_num : message_text}).encode()


client.connect()
client.publish(topic, generate_message(msg_num, message_text))
client.disconnect()

while True:
    msg_num += 1
    message_text = str(random.randint(0, 65536))

    client.connect()
    client.publish(topic, generate_message(msg_num, message_text))
    client.disconnect()
    time.sleep(2)
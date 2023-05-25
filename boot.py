#from util import setup_I2C_bus
from soil_moisture import Moisture_Sensor
import utime
from network_setup import Networker
from umqtt.simple import MQTTClient

#i2c = setup_I2C_bus()
#print("I2C bus established")

wlan = Networker().establish_connection()
print("wifi connection established")

client = MQTTClient('sensor_board_1', '10.42.0.1', port=1883, keepalive=60)
print("mqtt broker connection established")

test_ms = Moisture_Sensor(mqtt_handle=client)

while True:
#    test_ms = Moisture_Sensor(mqtt_handle=client)
    test_ms.read_moisture()
    test_ms.publish()
    utime.sleep(2)
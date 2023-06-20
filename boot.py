from air_quality import SGP30
from umqtt.simple import MQTTClient
from network_setup import Networker
from util import setup_I2C_bus
import utime

print("trying to connect....")
try:
    wlan = Networker().establish_connection()
    print("wlan")
except Exception as e:
   raise e

client = MQTTClient('aq_board_D', '10.42.0.1', port=1883, keepalive=60)
print("mqtt")

i2c_0 = setup_I2C_bus(bus_num='bus_0')
print("i2c_0")

i2c_1 = setup_I2C_bus(bus_num='bus_1')
print("i2c_1")

aq_1 = SGP30(bus=i2c_0, mqtt_handler=client, sensor_id='aq_D1')
aq_1.initAirQuality()

aq_2 = SGP30(bus=i2c_1, mqtt_handler=client, sensor_id='aq_D2')
aq_2.initAirQuality()

while True:
   aq_1.publish()
   aq_2.publish()
   utime.sleep_ms(500)
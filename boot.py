#
from machine import WDT
from air_quality import SGP30
from umqtt_simple import MQTTClient
from network_setup import Networker
from util import setup_I2C_bus
import utime

# watchdog timer to reset if errors
wdt = WDT()

# network connection

print("trying to connect....")
try:
    wlan = Networker().establish_connection()
    print("wlan")
except Exception as e:
   raise e

# MQTT stuff
SENSOR_ID = 'TESTING_C3'
BROKER_ADDR =  '192.168.10.1'
client = MQTTClient(SENSOR_ID, BROKER_ADDR, port=1883, keepalive=10)
print("mqtt")

i2c_0 = setup_I2C_bus(bus_num='bus_0')
print("i2c_0")

aq_1 = SGP30(bus=i2c_0, mqtt_handler=client, sensor_id=SENSOR_ID)
aq_1.initAirQuality()

while True:
   aq_1.publish()
   wdt.feed()
   utime.sleep_ms(200)

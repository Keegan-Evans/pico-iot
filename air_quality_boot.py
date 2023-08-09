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

try:
    wlan = Networker().establish_connection()
    print("wlan")
except Exception as e:
   raise e

# MQTT stuff
SENSOR_ID = 'air_quality'
BROKER_ADDR =  '10.42.0.1'
client = MQTTClient(SENSOR_ID, BROKER_ADDR, port=1883, keepalive=10)

i2c_0 = setup_I2C_bus(bus_num='bus_0')

aq_0 = SGP30(bus=i2c_0, mqtt_handler=client, sensor_id=SENSOR_ID)
aq_0.initAirQuality()

while True:
   aq_0.publish()
   wdt.feed()
   utime.sleep_ms(200)

##from soil_moisture import Moisture_Sensor
#import utime
#from network_setup import Networker
##from umqtt.simple import MQTTClient
#from util import setup_I2C_bus
#from air_quality import SGP30
#
#
#wlan = Networker().establish_connection()
#print("wifi connection established")
#
#client = MQTTClient('sensor_board_1', '10.42.0.1', port=1883, keepalive=60)
#print("mqtt broker connection established")
#
#i2c = setup_I2C_bus()
#print("I2C bus established")
#test_aq = SGP30(bus=i2c, mqtt_handler=client)
#
##test_ms = Moisture_Sensor(mqtt_handle=client)
#
#while True:
#    test_aq.publish()
##    test_ms = Moisture_Sensor(mqtt_handle=client)
##    test_ms.read_moisture()

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

client = MQTTClient('aq_board', '10.42.0.1', port=1883, keepalive=60)
print("mqtt")

i2c = setup_I2C_bus()
print("i2c")

test_aq = SGP30(bus=i2c, mqtt_handler=client)
test_aq.initAirQuality()

while True:
   print(test_aq.measurements())
   test_aq.publish()
   utime.sleep_ms(500)
# Ensure pico has correct libraries installed
from umqtt_simple import MQTTClient

#### Your Sensor Modules
#from <your_sensor_file> import <YourSensorClass>

### Device Setup Modules
from util import setup_I2C_bus, Networker

### built-in modules
import utime

### Setup Pico
# Setup Wifi
print("Connecting to wifi...")
wlan = Networker().establish_connection()
print("Wifi Connection Established")

# Setup I2C buses
print("Setting up I2C buses...")
I2C, device_bus_number = setup_I2C_bus(bus_num='bus_0')
print("I2C bus #{} establis".format(device_bus_number))

# Setup MQTT
client = MQTTClient('aq_D', '10.42.0.1', port=1883, keepalive=15)
print("mqtt")

#### Setup Sensors
#sensor = <YourSensorClass>(bus=i2c_0, mqtt_handler=client, sensor_id='aq_D1')

#while True:
#   sensor.publish()

   # additional housekeeping code
   # addiotional code for sleep/power management

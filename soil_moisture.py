# air_quality.py
from machine import Pin, ADC
from util import try_until_runs, set_timeout
import utime
import json

adc = ADC(Pin(28))
print(adc.read_u16())

class Moisture_Sensor:
    def __init__(self, mqtt_handler=None, sensor_pin=28, indicator_pin="LED", topic="sensor_data/soil_moisture", sensor_id="soil_moisture_1"):
        utime.sleep_ms(10)
        
        self.sensor_id = sensor_id
        self.topic = topic
        self.pin = ADC(Pin(sensor_pin))
        self._raw_value = 0
        self.calibration_value_low = 0
        self.calibration_value_high = 65535
        self.indicator_pin = Pin(indicator_pin, Pin.OUT)
        self.mqtt_handler = mqtt_handler
        self.topic = topic
        self.sensor_id = sensor_id

    def read_moisture(self):
        self.indicator_pin.on()
        self._raw_value = self.pin.read_u16()
        utime.sleep(1)
        self.indicator_pin.off()
        print(self._raw_value)
        if self.mqtt_handler is None:
            return self._raw_value
        else:
            return None

    def publish(self):
       if self.mqtt_handler is not None:
           self.read_moisture()
           msg = json.dumps({self.sensor_id : (self._raw_value / self.calibration_value_high)})
           self.mqtt_handler.connect()
           self.mqtt_handler.publish(self.topic, msg)
           self.mqtt_handler.disconnect()
       else:
           raise AttributeError("No MQTT handler defined for this sensor")

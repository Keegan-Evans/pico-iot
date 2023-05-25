from machine import Pin, I2C
from umqtt.simple import MQTTClient
import json

import utime

class Sensor:
    def __init__(self, mqtt_handle: MQTTClient,  sensor_id: str, topic: str, indicator_pin="LED"):
        utime.sleep_us(100)

        self.mqtt_handle = mqtt_handle
        self.sensor_id = sensor_id
        self.topic = topic
        self.indicator_pin = Pin(indicator_pin, Pin.OUT)

class AnalogSensor(Sensor):
    pass

class DigitalSensor(Sensor):
    def __init__(self, bus: I2C, *args, **kwargs):
        super.__init__(args, kwargs)
        self.bus = bus
    pass
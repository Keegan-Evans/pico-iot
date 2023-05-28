from util import try_until_runs, set_timeout
from machine import Pin, I2C
from umqtt.simple import MQTTClient
import json
from crc import create_message_packet

import utime

class Sensor:
    def __init__(self, device_name: str, mqtt_handler, topic: str, indicator_pin="LED"):

        self.mqtt_handler = mqtt_handler
        self.topic = topic
        self.indicator_pin = Pin(indicator_pin, Pin.OUT)
        self.measurements = json
        self.device_name = device_name

        utime.sleep_us(100)

        self.intialize_sensor()
    
    def intialize_sensor(self):
        self.indicator_pin.on()
    
    def measure(self):
        raise NotImplementedError

    def publish_to_broker(self):
        self.mqtt_handler.connect()
        self.mqtt_handler.publish(topic = self.topic.encode('utf-8'),
                                  msg = self.measurements)

class AnalogSensor(Sensor):
    def __init__(self, measurement_pin, *args, **kwargs):
        super.__init__(args, kwargs)
        self.measurement_pin = measurement_pin

class DigitalSensor(Sensor):
    def __init__(self, bus: I2C, bus_addr, use_checksums = False, *args, **kwargs):
        super.__init__(args, kwargs)
        self.bus = bus
        self.bus_addr = bus_addr
        self.use_checksums = use_checksums
        self.recent_readings = bytearray()

    @set_timeout(10)
    @try_until_runs
    def write_i2c(self, msg):
        if self.use_checksums == True:
            msg = create_message_packet(msg)
        elif type(msg) != bytes:
            msg = msg.encode('utf-8')

        self.bus.writeto(self.bus_addr, msg)
    
    @set_timeout(10)
    @try_until_runs
    def read_i2c(self, num_bytes):
        readings = bytearray(num_bytes)
        self.bus.readfrom_into(self.bus_addr, readings)
        self.recent_readings = readings
        return self.recent_readings
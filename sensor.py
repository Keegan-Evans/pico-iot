from machine import Pin
import utime
from util import set_timeout, try_until_runs, try_until_runs

# I want to refactor the publish method in the class Sensor already defined in this file so that it is only run at specified intervals, as well as adding a method for only updating the measurement values. I also want to initialize the class by handing measurement fields in as an iterable

class Sensor:
    def __init__(self, bus, mqtt_handler, i2c_address, indicator_pin, topic, sensor_id, checksum_method = None):
        self.i2c_address = i2c_address
        self.bus = bus
        self.mqtt_handler = mqtt_handler
        self.indicator_pin = Pin(indicator_pin, Pin.OUT)
        self.topic = topic
        self.sensor_id = sensor_id
        self.start_time = utime.mktime(utime.localtime())
        self.checksum_method = checksum_method
        self.elapsed_time = 0
        
    def set_elapsed_time(self):
        self.elapsed_time = utime.mktime(utime.localtime()) - self.start_time

    @set_timeout(10)
    @try_until_runs
    def write(self, msg):
        if self.checksum_method is not None:
            msg = self.checksum_method(msg)
        self.bus.writeto(self.i2c_address, msg)

    @set_timeout(10)
    @try_until_runs
    def read(self, num_bytes):
        readings = bytearray(num_bytes)
        self.bus.readfrom_into(self.i2c_address, readings)
        return readings

    def measurements(self):
        pass

    def publish(self):
        self.mqtt_handler.connect()
        self.mqtt_handler.publish(topic=bytes(self.topic, 'utf-8'), msg=self.measurements(), qos=0)
        self.mqtt_handler.disconnect()

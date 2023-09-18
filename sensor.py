from util import try_until_runs
from machine import Pin, ADC
import utime
import json


class AnalogSensor:
    def __init__(self, name, pin):
        self.pin = ADC(Pin(pin))
        self.name = name

    def get_reading(self):
        return self.pin.read_u16()


class Sensor:
    def __init__(
        self,
        mqtt_handler,
        topic,
        sensor_id,
        measurements,
        bus=None,
        i2c_address=None,
        indicator_pin="LED",
        checksum_method=None,
    ):
        self.i2c_address = i2c_address
        self.bus = bus
        self.mqtt_handler = mqtt_handler
        self.indicator_pin = Pin(indicator_pin, Pin.OUT)
        self.topic = topic
        self.sensor_id = sensor_id
        self.start_time = utime.mktime(utime.localtime())
        self.checksum_method = checksum_method
        self.elapsed_time = 0
        self.sensors = measurements
        # self.display = SevenSegmentDisplay(15, [17,16,14,13,12,18,19])

    def measurements(self):
        measurements = json.dumps(
            {
                "sensor": self.sensor_id,
                "data": {
                    sensor.name: sensor.get_reading()
                    for sensor in self.sensors
                },
            }
        )
        print(measurements)
        return measurements

    @try_until_runs
    def write(self, msg):
        if self.checksum_method is not None:
            msg = self.checksum_method(msg)
        self.bus.writeto(self.i2c_address, msg)

    @try_until_runs
    def read(self, num_bytes):
        readings = bytearray(num_bytes)
        self.bus.readfrom_into(self.i2c_address, readings)
        return readings

    def publish(self):
        self.mqtt_handler.connect()
        self.mqtt_handler.publish(
            topic=bytes(self.topic, "utf-8"), msg=self.measurements(), qos=0
        )
        self.mqtt_handler.disconnect()

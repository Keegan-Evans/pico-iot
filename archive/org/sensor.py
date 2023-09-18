import machine
from machine import Pin
import utime
from util import set_timeout, try_until_runs, try_until_runs

# I want to refactor the publish method in the class Sensor already defined in this file so that it is only run at specified intervals, as well as adding a method for only updating the measurement values. I also want to initialize the class by handing measurement fields in as an iterable

class SevenSegmentDisplay:
    def __init__(self, dot_pin, segment_pin_list):
        self.dot_pin = machine.Pin(dot_pin, machine.Pin.OUT)
        self.segment_pin_list = segment_pin_list
        self.pins = {}

        for idx, pin_num in enumerate(segment_pin_list):
            self.pins[pin_num] = (machine.Pin(pin_num, machine.Pin.OUT))


    def display_value(self, value):
        char_table = {
            "0": [1,1,1,1,1,1,0],
            "1": [0,1,1,0,0,0,0],
            "2": [1,1,0,1,1,0,1],
            "3": [1,1,1,1,0,0,1],
            "4": [0,1,1,0,0,1,1],
            "5": [1,0,1,1,0,1,1],
            "6": [1,0,1,1,1,1,1],
            "7": [1,1,1,0,0,0,0],
            "8": [1,1,1,1,1,1,1],
            "9": [1,1,1,1,0,1,1],
            "A": [1,1,1,0,1,1,1],
            "B": [0,0,1,1,1,1,1],
            "C": [1,0,0,1,1,1,0],
            "D": [0,1,1,1,1,0,1],
            "E": [1,0,0,1,1,1,1],
            "F": [1,0,0,0,1,1,1],
        }

        for idx, val in enumerate(char_table[value]):
            self.pins[self.segment_pin_list[idx]] = val


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
        self.display = SevenSegmentDisplay(15, [17,16,14,13,12,18,19])
        
    def set_elapsed_time(self):
        self.elapsed_time = utime.mktime(utime.localtime()) - self.start_time

    def display_error_code(self, vals):
        allowed_vals = [hex(x) for x in range(16)]

        if len(vals) == 2:
            for val in vals:
                if val not in allowed_vals:
                    raise ValueError("Value {} not allowed".format(val))
                else:
                    self.display.display_value(val)


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

    def parse_error_code(self, err):
        # TODO: create a lookup table for error codes
        # create a lookup table for error codes

        error_lookup_table = {
            # network errors
            # mqtt errors
            # i2c errors
            # sensor errors
            # other errors
            
        }
        error_code = error_lookup_table[err]

        # TODO: initialize 7 segment display on pico to display error codes
        display_error_code(error_code)

        # TODO: create a method for displaying error codes on the 7 segment display

        # TODO: Use the lookup table to display the error code on the 7 segment display
        

    # write test code for seven_segment_display




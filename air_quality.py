# air_quality.py

from util import try_until_runs, set_timeout
import utime
from crc import create_message_packet

INIT_AIR_QUALITY = bytearray([0x20, 0x03])
MEASURE_AIR_QUALITY = bytearray([0x20, 0x08])
MEASURE_RAW_SIGNALS = bytearray([0x20, 0x50])

class SGP30:
    def __init__(self, bus, mqtt_connection, address=0x58):
        utime.sleep_ms(1)

        self.address = address
        self.bus = bus
        self.mqtt = mqtt_connection
        self.co2 = None
        self.tvoc = None
        self.featureSetVersion = None
        self.h2 = None
        self.ethanol = None
        self.serialID = None
        self.start_time = utime.mktime(utime.localtime())
        self.elapsed_time = 0

    
    def set_elapsed_time(self):
        self.elapsed_time = utime.mktime(utime.localtime()) - self.start_time

    @set_timeout(10)
    @try_until_runs
    def write(self, msg):
        self.bus.writeto(self.address, create_message_packet(msg))

    @set_timeout(10)
    @try_until_runs
    def read(self, num_bytes):
        readings = bytearray(num_bytes)
        self.bus.readfrom_into(self.address, readings)
        return readings

    
    def initAirQuality(self):
        self.write(INIT_AIR_QUALITY)


    def measureAirQuality(self):
        self.write(MEASURE_AIR_QUALITY)
        # gives sensor time to record measurements, min 20-25ms
        utime.sleep_ms(50)
        read_vals = self.read(6)
        self.set_elapsed_time()
        
        # No real values are returned for the co2 or tvoc values until
        # 15 seconds after the initialization of the sensor so that
        # proper calibration can occur
        if self.elapsed_time < 15:
            self.co2 = bytearray([255 << 8 | 255])
            self.tvoc = bytearray([255 << 8 | 255])
        self.co2 = bytearray([read_vals[0] << 8 | read_vals[1]])
        self.tvoc= bytearray([read_vals[3] << 8 | read_vals[4]])
        return None


    def measureRawSignals(self):
        self.write(MEASURE_RAW_SIGNALS)
        # gives sensor time to record measurements, min 20-25ms
        utime.sleep_ms(50)
        read_vals = self.read(6)
        self._h2 = bytearray([read_vals[0] << 8 | read_vals[1]])
        self.ethanol = bytearray([read_vals[3] << 8 | read_vals[4]])
        return None

    
    @property
    def measurements(self):
        self.measureRawSignals()
        self.measureAirQuality()

        measurement_values = {'co2': int.from_bytes(self.co2, 'big'),
                              'tvoc': int.from_bytes(self.tvoc, 'big'),
                              'h2': int.from_bytes(self.h2, 'big'),
                              'ethanol': int.from_bytes(self.ethanol, 'big'),
                              'elapsed_time': self.elapsed_time
                              }

    def report_measurements(self):
        pass

        

if __name__ == '__main__':
    from util import setup_I2C_bus

    i2c = setup_I2C_bus()

    test_aq = SGP30(bus=i2c)

    while True:
        print(test_aq.measurements)
        utime.sleep_ms(250)

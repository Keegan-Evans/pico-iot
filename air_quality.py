# air_quality.py

from _util import try_until_runs, set_timeout
import time
from crc import create_message_packet

INIT_AIR_QUALITY = bytearray([0x20, 0x03])
MEASURE_AIR_QUALITY = bytearray([0x20, 0x08])
MEASURE_RAW_SIGNALS = bytearray([0x20, 0x50])

class SGP30:
    def __init__(self, bus, address=0x58):
        time.sleep_ms(1)

        self.address = address
        self.bus = bus
        self._co2 = None
        self._tvoc = None
        self.featureSetVersion = None
        self._h2 = None
        self._ethanol = None
        self.serialID = None

    
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
        time.sleep_ms(50)
        read_vals = self.read(6)
        self._co2 = bytearray([read_vals[0] << 8 | read_vals[1]])
        self._tvoc= bytearray([read_vals[3] << 8 | read_vals[4]])
        return None


    def measureRawSignals(self):
        self.write(MEASURE_RAW_SIGNALS)
        # gives sensor time to record measurements, min 20-25ms
        time.sleep_ms(50)
        read_vals = self.read(6)
        self._h2 = bytearray([read_vals[0] << 8 | read_vals[1]])
        self._ethanol = bytearray([read_vals[3] << 8 | read_vals[4]])
        return None

    
    @property
    def CO2(self):
        return int.from_bytes(self._co2, 'big')
 

    @property
    def TVOC(self):
        return int.from_bytes(self._tvoc, 'big')
 

    @property
    def H2(self):
        return int.from_bytes(self._h2, 'big')
 

    @property
    def ethanol(self):
        return int.from_bytes(self._ethanol, 'big')

if __name__ == '__main__':
    from _util import setup_I2C_bus

    i2c = setup_I2C_bus()

    test_aq = SGP30(bus=i2c)
    test_aq.start_measuring_aq()

    while True:
        print("CO2: {}\nVOC: {}\nH2: {}\nEthanol: {}\n\n".format(test_aq.CO2, test_aq.TVOC, test_aq.H2, test_aq.ethanol))
        time.sleep(5)
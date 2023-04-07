# air_quality.py

from _util import try_until_runs, SUCCESS, FAILURE, set_timeout
import time

INIT_AIR_QUALITY = bytearray([0x20, 0x03])
MEASURE_AIR_QUALITY = bytearray([0x20, 0x08])
GET_BASELINE = bytearray([0x20, 0x15])
SET_BASELINE = bytearray([0x20, 0x1E])
#SET_HUMIDITY = bytearray([0x20, 0x61])
MEASURE_TEST = bytearray([0x20, 0x32])
#GET_FEATURE_SET_VERSION = bytearray([0x20, 0x2F])
GET_SERIAL_ID = bytearray([0X36, 0x82])
MEASURE_RAW_SIGNALS = bytearray([0x20, 0x50])
CRC_LOOKUP_TABLE = [
      [0x00, 0x31, 0x62, 0x53, 0xC4, 0xF5, 0xA6, 0x97, 0xB9, 0x88, 0xDB, 0xEA, 0x7D, 0x4C, 0x1F, 0x2E],
      [0x43, 0x72, 0x21, 0x10, 0x87, 0xB6, 0xE5, 0xD4, 0xFA, 0xCB, 0x98, 0xA9, 0x3E, 0x0F, 0x5C, 0x6D],
      [0x86, 0xB7, 0xE4, 0xD5, 0x42, 0x73, 0x20, 0x11, 0x3F, 0x0E, 0x5D, 0x6C, 0xFB, 0xCA, 0x99, 0xA8],
      [0xC5, 0xF4, 0xA7, 0x96, 0x01, 0x30, 0x63, 0x52, 0x7C, 0x4D, 0x1E, 0x2F, 0xB8, 0x89, 0xDA, 0xEB],
      [0x3D, 0x0C, 0x5F, 0x6E, 0xF9, 0xC8, 0x9B, 0xAA, 0x84, 0xB5, 0xE6, 0xD7, 0x40, 0x71, 0x22, 0x13],
      [0x7E, 0x4F, 0x1C, 0x2D, 0xBA, 0x8B, 0xD8, 0xE9, 0xC7, 0xF6, 0xA5, 0x94, 0x03, 0x32, 0x61, 0x50],
      [0xBB, 0x8A, 0xD9, 0xE8, 0x7F, 0x4E, 0x1D, 0x2C, 0x02, 0x33, 0x60, 0x51, 0xC6, 0xF7, 0xA4, 0x95],
      [0xF8, 0xC9, 0x9A, 0xAB, 0x3C, 0x0D, 0x5E, 0x6F, 0x41, 0x70, 0x23, 0x12, 0x85, 0xB4, 0xE7, 0xD6],
      [0x7A, 0x4B, 0x18, 0x29, 0xBE, 0x8F, 0xDC, 0xED, 0xC3, 0xF2, 0xA1, 0x90, 0x07, 0x36, 0x65, 0x54],
      [0x39, 0x08, 0x5B, 0x6A, 0xFD, 0xCC, 0x9F, 0xAE, 0x80, 0xB1, 0xE2, 0xD3, 0x44, 0x75, 0x26, 0x17],
      [0xFC, 0xCD, 0x9E, 0xAF, 0x38, 0x09, 0x5A, 0x6B, 0x45, 0x74, 0x27, 0x16, 0x81, 0xB0, 0xE3, 0xD2],
      [0xBF, 0x8E, 0xDD, 0xEC, 0x7B, 0x4A, 0x19, 0x28, 0x06, 0x37, 0x64, 0x55, 0xC2, 0xF3, 0xA0, 0x91],
      [0x47, 0x76, 0x25, 0x14, 0x83, 0xB2, 0xE1, 0xD0, 0xFE, 0xCF, 0x9C, 0xAD, 0x3A, 0x0B, 0x58, 0x69],
      [0x04, 0x35, 0x66, 0x57, 0xC0, 0xF1, 0xA2, 0x93, 0xBD, 0x8C, 0xDF, 0xEE, 0x79, 0x48, 0x1B, 0x2A],
      [0xC1, 0xF0, 0xA3, 0x92, 0x05, 0x34, 0x67, 0x56, 0x78, 0x49, 0x1A, 0x2B, 0xBC, 0x8D, 0xDE, 0xEF],
      [0x82, 0xB3, 0xE0, 0xD1, 0x46, 0x77, 0x24, 0x15, 0x3B, 0x0A, 0x59, 0x68, 0xFF, 0xCE, 0x9D, 0xAC]]

class SGP30:
    def __init__(self, bus, address=0x58):
        self.address = address
        self.bus = bus
        self._co2 = ReceivedValue()
        self._tvoc = ReceivedValue()
        self.featureSetVersion = ReceivedValue()
        self._h2 = ReceivedValue()
        self._ethanol = ReceivedValue()
        self.serialID = ReceivedValue()
        
    def CRC_lookup(self, data):
        CRC = 0xFF
        CRC ^= data >> 8
        CRC = CRC_LOOKUP_TABLE[CRC >> 4][CRC & 0xF]
        CRC ^= data
        CRC = CRC_LOOKUP_TABLE[CRC >> 4][CRC & 0xF]
        return CRC
        

    @set_timeout(10)
    @try_until_runs
    def write(self, buffer):
        return self.bus.writeto(self.address, buffer)

    @set_timeout(10)
    @try_until_runs
    def read(self, num_bytes):
        readings = bytearray(num_bytes)
        self.bus.readfrom_into(self.address, readings)
        #readings = tuple((reading for reading in readings))
        return readings
    
    def init_AirQuality(self):
        self.write(INIT_AIR_QUALITY)

    def measureAirQuality(self):
        self.write(MEASURE_AIR_QUALITY)
        time.sleep_ms(25)
        read_vals = self.read(6)
        self._co2 = read_vals[0] << 8 | read_vals[1]
        self._tvoc = read_vals[4] << 8 | read_vals[5]
        try:
            self.C02.validate_checksum(read_vals[2])
            self._tvoc.validate_checksum(read_vals[5])
            return SUCCESS
        except ValidationError:
            raise ve
        except Exception as e:
            raise e
        
    def getBaseline(self):
        self.write(GET_BASELINE)
        time.sleep_ms(10)

        read_vals = self.read(6)

        self.baseline__co2 = read_vals[0] << 8 | read_vals[1]
        self.baseline__tvoc = read_vals[3] << 8 | read_vals[4]

        try:
            self.baseline__co2.validate_checksum(read_vals[2])
            self.baseline__tvoc.validate_checksum(read_vals[5])
            return SUCCESS
        except ValidationError as ve:
            raise ve
        except Exception as e:
            raise e

    def setBaseline(self):
        """Used to update the baseline values that the SGP30 chip is using to
        calculate calibrated values. Enables more accurate reading nearly
        immeadiately on startup"""

        # If there are no values to use as a baseline, go ahead and get them
        if self.baseline__co2 | self.baseline__tvoc is None:
            self.getBaseline()

        # now actually send them to the SGP30 to be stored
        # Be sure to include the checksum calculations so that the SGP30 accepts the values.
        baseline_vals = bytearray([self.baseline__tvoc >> 8, self.baseline__tvoc, self.CRC_lookup(self.baseline__tvoc),
                                   self.baseline__co2 >> 8, self.baseline__co2, self.CRC_lookup(self.baseline__co2)])

        self.write(SET_BASELINE)
        self.write(baseline_vals)


    def measureRawSignals(self):
        self.write(MEASURE_RAW_SIGNALS)
        # gives sensor time to record measurements, min 20-25ms
        time.sleep_ms(25)
        read_vals = self.read(6)
        self._h2 = read_vals[0] << 8 | read_vals[1]
        self._ethanol = read_vals[3] << 8 | read_vals[4]

        try:
            self._h2.validate_checksum(read_vals[2])
            self._ethanol.validate_checksum(read_vals[5])
        except ValidationError as ve:
            raise ve
        except Exception as e:
            raise e
    
    def set_humidity_compensation(self, comp_value):
        """NEED HUMIDITY SENSOR CONNECTED TO SYSTEM FOR THIS, comp_value should be a 16-bit unsigned integer"""
        self.write(SET_HUMIDITY)
        humidity_bytes = bytearray([comp_value >>8, comp_value, self.CRC_lookup(comp_value)])
        self.write(humidity_bytes)
    
    def getSerialID(self):

        self.write(GET_SERIAL_ID)
        time.sleep_ms(10)

        read_data = self.read(9)

        try:
            serial1 = self._process_bytes_and_checksums(read_data[0:2])
            serial2 = self._process_bytes_and_checksums(read_data[3:5])
            serial3 = self._process_bytes_and_checksums(read_data[6:8])
        except ValidationError:
            self.getSerialID()
        except Exception as e:
            raise e

        self.getSerialID = serial1 << 32 + serial2 << 16 + serial3


    def selfTest(self):
        """Call the SGP30 builtin self test"""
        self.write(MEASURE_TEST)

        # data sheet shows to give the test >200ms delay
        time.sleep_ms(500)

        try:
            self._process_bytes_and_checksums(self.read(3))
            return SUCCESS
        except Exception as e:
            raise e

    def _process_bytes_and_checksums(self, input_bytes):
        read_value = bytearray([input_bytes[0] << 8 | input_bytes[1]])
        checksum = input_bytes[2]

        try:
            assert self.CRC_lookup(read_value) == checksum
            return read_value
        except:
            raise ValidationError("There was a problem with the received data")




    @property
    def CO2(self):
        if self._co2 is None:
            self.measureAirQuality()

        return self._co2
 
    @property
    def TVOC(self):
        if self._tvoc is None:
            self.measureAirQuality()

        return self._tvoc 
 
    @property
    def H2(self):
         if self._h2 is None:
             self.measureRawSignals()
         return self._h2 
 
    @property
    def ethanol(self):
        if self._ethanol is None:
            self.measureRawSignals()
        return self._ethanol 


class ReceivedValue:
    def __init__(self, val=None):
        self.val = val
    def validate_checksum(self, checksum):
        try:
            assert self.val == checksum
        except:
            raise ValidationError("The observed value does not match checksum: {} != {}".format(self.val, checksum))

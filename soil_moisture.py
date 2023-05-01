from machine import Pin, ADC
import json

import time

adc = ADC(Pin(28))
print(adc.read_u16())
#print(adc.read_uv())

class Moisture_Sensor:
    def __init__(self, pin_num=28, group="test", topic="sensor", indicator_pin=16):
        time.sleep_us(100)
        
        self.group = group
        self.topic = topic
        self.pin = ADC(Pin(pin_num))
        self._raw_value = None
        self.calibration_value_low = 0
        self.calibration_value_high = 65535
        self.indicator_pin = Pin(1, Pin.OUT)
        
    @property
    def raw_read(self):
        self.indicator_pin.on()
        self._raw_value = self.pin.read_u16()
        time.sleep(1)
        self.indicator_pin.off()
        return self._raw_value.to_bytes(2, 'big')

    @property
    def packaged_read(self):
        self.indicator_pin.on()
        read = ''
        json.dump(self.raw_read, read, (',', ':'))
        time.sleep(0.25)
        return read
    
    #def set_low_calibration(self):
    #    self.indicator_pin.on()
    #    calibration_reads = []
    #    #Pin(25).on()
    #    for t in range(10):
    #        time.sleep(2)
    #        read = self.raw_read
    #        print(read)
    #        calibration_reads.append(read)
    #        
    #    calibration_reads.remove(max(calibration_reads))
    #    calibration_reads.remove(min(calibration_reads))
    #        
    #    self.calibration_value_low = sum(calibration_reads)/len(calibration_reads)
    #    self.indicator_pin.off()
    #    
    #    
    #def set_high_calibration(self):
    #    self.indicator_pin.on()
    #    calibration_reads = []
    #    for t in range(10):
    #        time.sleep(2)
    #        #Pin(25).off()
    #        calibration_reads.append(self.raw_read)
    #        #Pin(25).on()
    #        print(calibration_reads)
    #        
    #    calibration_reads.remove(max(calibration_reads))
    #    calibration_reads.remove(min(calibration_reads))
    #        
    #    self.calibration_value_high = sum(calibration_reads)/len(calibration_reads)
    #    print(self.calibration_value_high)
    #    self.indicator_pin.off()
    #    
    #
    #
    #def calibrated_read(self):
    #    p1 = (0, self.calibration_value_low)
    #    p2 = (100, self.calibration_value_high)
    #    m = (p2[1] - p1[1])/(p2[0] - p1[0])
    #    
    #    x = ((self.raw_read - p1[1])/m)
    #    return x
            
if __name__ == '__main__':
    test_ms = Moisture_Sensor()
    b = test_ms.raw_read
    print(b)

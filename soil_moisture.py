from machine import Pin, ADC
import json

import time
# from ulab import numpy as np
# import array
#
adc = ADC(Pin(28))
print(adc.read_u16())
#print(adc.read_uv())

class Moisture_Sensor:
    def __init__(self, mqtt_handle, pin_num=28, sensor_id="soil_moisture_1", topic="sensor", indicator_pin="LED"):
       time.sleep_us(100)

       self.sensor_id = sensor_id
       self.topic = topic
       self.pin = ADC(Pin(pin_num))
       self._raw_value = 0
       self.calibration_value_low = 0
       self.calibration_value_high = 65535
       self.indicator_pin = Pin(indicator_pin, Pin.OUT)
       self.mqtt_handle = mqtt_handle
       
    def toggle_indicator(self):
        self.indicator_pin.toggle()
       
    def read_moisture(self):
        self.indicator_pin.on()
        self._raw_value = self.pin.read_u16()
        time.sleep(1)
        self.indicator_pin.off()
        print(self._raw_value)
        return None
        # return self._raw_value.to_bytes(2, 'big')

    def publish(self):
        self.read_moisture()
        msg = json.dumps({self.sensor_id : (self._raw_value / self.calibration_value_high)})
        self.mqtt_handle.connect()
        self.mqtt_handle.publish(self.topic, msg)
        self.mqtt_handle.disconnect()


 
    
    # def set_low_calibration(self):
    #     self.indicator_pin.on()
    #     calibration_reads = []
    #     #Pin(25).on()
    #     for t in range(10):
    #         time.sleep(2)
    #         read = self.raw_read
    #         print(read)
    #         calibration_reads.append(read)
            
    #     calibration_reads.remove(max(calibration_reads))
    #     calibration_reads.remove(min(calibration_reads))
            
    #     self.calibration_value_low = sum(calibration_reads)/len(calibration_reads)
    #     self.indicator_pin.off()
        
        
    # def set_high_calibration(self):
    #     self.indicator_pin.on()
    #     calibration_reads = []
    #     for t in range(10):
    #         time.sleep(2)
    #         #Pin(25).off()
    #         calibration_reads.append(self.raw_read)
    #         #Pin(25).on()
    #         print(calibration_reads)
            
    #     calibration_reads.remove(max(calibration_reads))
    #     calibration_reads.remove(min(calibration_reads))
            
    #     self.calibration_value_high = sum(calibration_reads)/len(calibration_reads)
    #     print(self.calibration_value_high)
    #     self.indicator_pin.off()
        
    
   
#    def calibrated_read(self):
#        p1 = (0, self.calibration_value_low)
#        p2 = (100, self.calibration_value_high)
#        m = (p2[1] - p1[1])/(p2[0] - p1[0])
       
#        x = ((self.raw_read - p1[1])/m)
#        return x

# def generate_calibration_line(min, max, intervals=100):
#     return np.array(range(min, max+1, (max - min)//intervals))

# def get_calibrated_value(raw_val,
#                          input_map,
#                          output_map):
#     rel_vals = map(lambda y: abs(y - raw_val), input_map)
#     print(list(rel_vals))
#     #rel_vals = lambda x: abs(input_map - raw_val)
#     rel_val = min(input_map, key=rel_vals)
#     return output_map[rel_val] 

# def closest_value(input_map, input_value):
#     mapped = [abs(x - input_value) for x in input_map]
#     return mapped
#     #print(mapped)
#     #i = mapped.argmin()
#     #print(i)
#     #print(arr[i])
            
if __name__ == '__main__':
    from test_setup import setup_for_testing
    from util import setup_I2C_bus
    wlan, client = setup_for_testing()
    i2c = setup_I2C_bus()

    while True:
        test_ms = Moisture_Sensor(mqtt_handle=client)
        test_ms.read_moisture()
        test_ms.publish()
        time.sleep(2)
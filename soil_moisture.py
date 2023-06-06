from machine import Pin, ADC
import json

import utime
#
adc = ADC(Pin(28))
print(adc.read_u16())
#print(adc.read_uv())

class Moisture_Sensor:
    def __init__(self, mqtt_handle=None, pin_num=28, sensor_id="soil_moisture_1", topic="sensor/moisture", indicator_pin="LED"):
       utime.sleep_us(100)

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
        utime.sleep(1)
        self.indicator_pin.off()
        print(self._raw_value)
        if self.mqtt_handle is None:
            return self._raw_value
        else:
            return None
        # return self._raw_value.to_bytes(2, 'big')

    def publish(self):
        if self.mqtt_handle is not None:
            self.read_moisture()
            msg = json.dumps({self.sensor_id : (self._raw_value / self.calibration_value_high)})
            self.mqtt_handle.connect()
            self.mqtt_handle.publish(self.topic, msg)
            self.mqtt_handle.disconnect()
        else:
            raise AttributeError("No MQTT handler defined for this sensor")


if __name__ == '__main__':
    test_ms = Moisture_Sensor()

    while True:
        reading = test_ms.read_moisture()
        print(reading)
        utime.sleep(2)

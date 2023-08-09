# air_quality.py
from machine import Pin, ADC
from util import try_until_runs, set_timeout
import utime
from crc import create_message_packet
from umqtt_simple import MQTTClient
import json

class WeatherStation:
    WMK_NUM_ANGLES = 16
    SFE_WIND_VANE_DEGREES_PER_INDEX = 22.5
    SFE_WIND_VANE_ADC_RESOLUTION_DEFAULT = 12

    def __init__(self, bus, mqtt_handler, i2c_address=0x58, indicator_pin="LED", windDirectionPin =26, rainfallPin=28, windSpeedPin=27, topic="sensor_data/air_quality", sensor_id="air_quality"):
        utime.sleep_ms(10)

        self.mqtt_handler = mqtt_handler
        self.indicator_pin = Pin(indicator_pin, Pin.OUT)
        self.topic = topic
        self.sensor_id = sensor_id

        self._windDirectionPin = ADC(Pin(windDirectionPin))
        self._windSpeedPin = Pin(windSpeedPin, Pin.IN, Pin.PULL_UP)
        self._rainfallPin = Pin(rainfallPin, Pin.IN, Pin.PULL_UP)

        self._calibrationParams = {
            "vaneADCValues": {
                0.0: 3143, 22.5: 1624, 45.0: 1845, 67.5: 335,
                90.0: 372, 112.5: 264, 135.0: 738, 157.5: 506,
                180.0: 1149, 202.5: 979, 225.0: 2520, 247.5: 2397,
                270.0: 3780, 292.5: 3309, 315.0: 3548, 337.5: 2810
            },
            "kphPerCountPerSec": 2.4,
            "windSpeedMeasurementPeriodMillis": 1000,
            "mmPerRainfallCount": 0.2794,
            "minMillisPerRainfall": 100
        }

        self._windCountsPrevious = 0
        self._windCounts = 0
        self._rainfallCounts = 0

        self._lastWindSpeedMillis = utime.ticks_ms()
        self._lastRainfallMillis = utime.ticks_ms()


    def measurements(self):
        self.indicator_pin.on()
        self.update_measurements()
        self.indicator_pin.off()

        measurement_values = json.dumps(
            {'sensor': self.sensor_id,
             'data':
                {'wind_speed': int.from_bytes(self.windspeed, 'big'),
                 'wind_direction': int.from_bytes(self.winddirection, 'big'),
                 'rain_fall': int.from_bytes(self.rainfall, 'big'),
                }})

        return measurement_values

    def update_measurements(self):
        self.rainfall = self.measure_rain()
        self.windspeed = self.measure_wind()
        self.winddirection = self.measure_wind_direction()

    def measure_rain(self):
        pass

    def measure_wind(self): 
        pass
    
    def measure_wind_direction(self):
        pass

    # ------------------------ CHATGPT DRAFT ------------------------
    def begin(self):
        self._windSpeedPin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.windSpeedInterrupt)
        self._rainfallPin.irq(trigger=Pin.IRQ_RISING, handler=self.rainfallInterrupt)

    def windSpeedInterrupt(self, pin):
        self._windCounts += 1

    def rainfallInterrupt(self, pin):
        self._rainfallCounts += 1

    def getWindDirection(self):
        rawADC = self._windDirectionPin.read()
        closestDifference = float("inf")
        closestIndex = 0

        for angle, adc_value in self._calibrationParams["vaneADCValues"].items():
            adcDifference = abs(adc_value - rawADC)

            if adcDifference < closestDifference:
                closestDifference = adcDifference
                closestIndex = angle

        return closestIndex

    def updateWindSpeed(self):
        tNow = utime.ticks_ms()
        dt = tNow - self._lastWindSpeedMillis

        if dt < self._calibrationParams["windSpeedMeasurementPeriodMillis"]:
            pass
        elif dt > (self._calibrationParams["windSpeedMeasurementPeriodMillis"] * 2):
            self._windCountsPrevious = 0
            self._windCounts = 0
            self._lastWindSpeedMillis = tNow
        else:
            self._windCountsPrevious = self._windCounts
            self._windCounts = 0
            self._lastWindSpeedMillis += self._calibrationParams["windSpeedMeasurementPeriodMillis"]

    def getWindSpeed(self):
        self.updateWindSpeed()

        windSpeed = float(self._windCountsPrevious) / self._calibrationParams["windSpeedMeasurementPeriodMillis"]
        windSpeed *= 1000 * self._calibrationParams["kphPerCountPerSec"] / 2

        return windSpeed

    def getRainfallAmount(self):
        return self._rainfallCounts * self._calibrationParams["mmPerRainfallCount"]


    

    def publish(self):
        self.mqtt_handler.connect()
        print(bytes(self.topic, 'utf-8'), "\n", self.measurements)
        self.mqtt_handler.publish(topic=bytes(self.topic, 'utf-8'), msg=self.measurements(), qos=1)
        self.mqtt_handler.disconnect()

#if __name__ == '__main__':
#    from umqtt.simple import MQTTClient
#    from network_setup import Networker
#    from util import setup_I2C_bus
#
#    wlan = Networker().establish_connection()
#    print("wlan")
#
#    client = MQTTClient('aq_board', '10.42.0.1', port=1883, keepalive=60)
#    print("mqtt")
#
#    i2c = setup_I2C_bus()
#    print("i2c")
#
#    test_aq = SGP30(bus=i2c, mqtt_handler=client)
#    test_aq.initAirQuality()
#
#    while True:
#
#       print(test_aq.measurements())
#       test_aq.publish()
#       utime.sleep_ms(180)
#
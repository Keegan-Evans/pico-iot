# weather_station.py
from machine import Pin, ADC  # , reset
from util import connect_network
import utime
from mqtt import MQTTClient
import json


class WeatherStation:
    WMK_NUM_ANGLES = 16
    SFE_WIND_VANE_DEGREES_PER_INDEX = 22.5
    SFE_WIND_VANE_ADC_RESOLUTION_DEFAULT = 12

    def __init__(
        self,
        mqtt_handler,
        indicator_pin="LED",
        windDirectionPin=27,
        rainfallPin=28,
        windSpeedPin=26,
        topic="sensor_data/weather_station",
        sensor_id="weather_station",
        reporting_interval=5,
    ):
        utime.sleep_ms(10)

        self.mqtt_handler = mqtt_handler
        self.indicator_pin = Pin(indicator_pin, Pin.OUT)
        self.topic = topic
        self.sensor_id = sensor_id
        self.reporting_interval = reporting_interval

        self._windDirectionPin = ADC(Pin(windDirectionPin))
        self._windSpeedPin = Pin(windSpeedPin, Pin.IN, Pin.PULL_UP)
        self._rainfallPin = Pin(rainfallPin, Pin.IN, Pin.PULL_UP)
        self.wind_direction = 0
        self.wind_speed = 0
        self.rainfall = 0

        self._calibrationParams = {
            "vaneADCValues": {
                0.0: 3143,
                22.5: 1624,
                45.0: 1845,
                67.5: 335,
                90.0: 372,
                112.5: 264,
                135.0: 738,
                157.5: 506,
                180.0: 1149,
                202.5: 979,
                225.0: 2520,
                247.5: 2397,
                270.0: 3780,
                292.5: 3309,
                315.0: 3548,
                337.5: 2810,
            },
            "kphPerCountPerSec": 2.4,
            "windSpeedMeasurementPeriodMillis": reporting_interval * 1000,
            "mmPerRainfallCount": 0.2794,
            "minMillisPerRainfall": 100,
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

        # weather station measurement values
        ws_measurement_values = json.dumps(
            {
                "sensor": self.sensor_id,
                "data": {
                    "wind_direction": self.raw_wind_direction,
                    "wind_speed": self.wind_speed,
                    "rainfall": self.rainfall,
                },
            }
        )

        return ws_measurement_values

    def update_measurements(self):
        self.measure_rain()
        self.measure_wind_speed()
        self.measure_wind_direction()

    def begin(self):
        self._windSpeedPin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
            handler=self.windSpeedInterrupt,
        )
        self._rainfallPin.irq(
            trigger=Pin.IRQ_RISING, handler=self.rainfallInterrupt
        )

    def windSpeedInterrupt(self, pin):
        self._windCounts += 1

    def rainfallInterrupt(self, pin):
        self._rainfallCounts += 1

    def measure_wind_direction(self):
        # use read_u16 as that is what the sparkfun arduino library uses
        rawADC = self._windDirectionPin.read_u16()
        self.raw_wind_direction = rawADC
        closestDifference = float(32767)
        closestIndex = 0

        for angle, adc_value in self._calibrationParams[
            "vaneADCValues"
        ].items():
            adcDifference = abs(adc_value - rawADC)

            if adcDifference < closestDifference:
                closestDifference = adcDifference
                closestIndex = angle

        self.wind_direction = closestIndex
        return None

    def measure_wind_speed(self):
        tNow = utime.ticks_ms()
        dt = tNow - self._lastWindSpeedMillis

        if dt < self._calibrationParams["windSpeedMeasurementPeriodMillis"]:
            pass
        elif dt > (
            self._calibrationParams["windSpeedMeasurementPeriodMillis"] * 2
        ):
            self._windCountsPrevious = 0
            self._windCounts = 0
            self._lastWindSpeedMillis = tNow
        else:
            self._windCountsPrevious = self._windCounts
            self._windCounts = 0
            self._lastWindSpeedMillis += self._calibrationParams[
                "windSpeedMeasurementPeriodMillis"
            ]

        self.wind_speed = (
            float(self._windCountsPrevious)
            / self._calibrationParams["windSpeedMeasurementPeriodMillis"]
        )
        self.wind_speed *= (
            1000 * self._calibrationParams["kphPerCountPerSec"] / 2
        )

        return None

    def measure_rain(self):
        self.rainfall = (
            self._rainfallCounts
            * self._calibrationParams["mmPerRainfallCount"]
        )
        return None

    def publish(self):
        # try:
        self.mqtt_handler.connect()
        self.mqtt_handler.publish(
            topic=bytes(self.topic, "utf-8"), msg=self.measurements(), qos=1
        )
        self.mqtt_handler.disconnect()
        utime.sleep(self.reporting_interval)
        # except OSError.errno == 113:
        #    reset()


if __name__ == "__main__":
    wlan = connect_network()
    SENSOR_ID = "weather_station_demo_1"
    BROKER_ADDR = "10.42.0.1"

    client = MQTTClient(SENSOR_ID, BROKER_ADDR, port=1883, keepalive=10)
    ws = WeatherStation(mqtt_handler=client)

    # test the wind speed funtions
    ws.begin()
    while True:
        ws.publish()
        utime.sleep(3)

# if __name__ == '__main__':
#     from umqtt.simple import MQTTClient
#     from network_setup import Networker
#     from util import setup_I2C_bus
#
#     wlan = Networker().establish_connection()
#     print("wlan")
#
#     client = MQTTClient('aq_board', '10.42.0.1', port=1883, keepalive=60)
#     print("mqtt")
#
#     i2c = setup_I2C_bus()
#     print("i2c")
#
#     test_aq = SGP30(bus=i2c, mqtt_handler=client)
#     test_aq.initAirQuality()
#
#     while True:
#
#        print(test_aq.measurements())
#        test_aq.publish()
#        utime.sleep_ms(180)
#

from machine import Pin, ADC
import time

class SFEWeatherMeterKit:
    WMK_NUM_ANGLES = 16
    SFE_WIND_VANE_DEGREES_PER_INDEX = 22.5
    SFE_WIND_VANE_ADC_RESOLUTION_DEFAULT = 12

    def __init__(self, windDirectionPin, windSpeedPin, rainfallPin):
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

        self._lastWindSpeedMillis = time.ticks_ms()
        self._lastRainfallMillis = time.ticks_ms()

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
        tNow = time.ticks_ms()
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

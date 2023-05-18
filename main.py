from util import setup_I2C_bus
from ser_lcd import SerLCD
import time
from network_setup import Networker
from air_quality import SGP30
import bme280_int

wlan = Networker.connection
i2c = setup_I2C_bus()

### environmental sensor
#environmental_sensor = bme280_int.BME280(i2c=i2c)
#print("environmental measurements:{}".format(environmental_sensor.values))

#my_lcd = SerLCD(bus=i2c)
# my_lcd.clear_screen()    
# my_lcd.contrast(180)
# my_lcd.increase_contrast()
# 
# my_aq = SGP30(bus=i2c)
# my_aq.initAirQuality()
# x = 15
# while x > 0:
#     my_aq.measureAirQuality()
#     my_aq.measureRawSignals()
#     co2_reading = my_aq.CO2
#     print(co2_reading)
#     #my_lcd.clear_screen()
#     #my_lcd.write("co2 reading: {}".format(co2_reading))
#     time.sleep_ms(500)
#     x -= 1
# 

#test_screen()
#test_aq_sensor()

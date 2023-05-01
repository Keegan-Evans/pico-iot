from _util import setup_I2C_bus
from ser_lcd import SerLCD
import time
from air_quality import SGP30

i2c = setup_I2C_bus()
my_lcd = SerLCD(bus=i2c)
time.sleep_ms(500)


# while True:
#     if my_lcd.contrast_pin.value() == 1:
#         my_lcd.increase_contrast()
  
   
my_lcd = SerLCD(bus=i2c)
#time.sleep_ms(50)
#my_lcd.clear_screen()    
#    my_lcd.hello_world()
#    my_lcd.contrast(180)
#    my_lcd.increase_contrast()
#    my_lcd.print_message(my_aq.read(6))

my_aq = SGP30(bus=i2c)
my_aq.initAirQuality()

my_aq.measureAirQuality()
co2_reading = my_aq.CO2
print(co2_reading)
#my_lcd.write("co2 reading: {}".format(co2_reading))


#test_screen()
#test_aq_sensor()

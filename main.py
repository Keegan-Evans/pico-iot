from _util import setup_I2C_bus
from ser_lcd import SerLCD
import time
from air_quality import SGP30

i2c = setup_I2C_bus()
my_lcd = SerLCD(bus=i2c)
my_lcd.clear_screen()    
my_lcd.contrast(180)
my_lcd.increase_contrast()

my_aq = SGP30(bus=i2c)
while True:
    co2_reading = my_aq.CO2
    print(co2_reading)
    my_lcd.clear_screen()
    my_lcd.write("co2 reading: {}".format(co2_reading))
    time.sleep(5)


#test_screen()
#test_aq_sensor()

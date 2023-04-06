from _util import setup_I2C_bus
#from ser_lcd import SerLCD
from airquality import SGP30, MEASURE_RAW_SIGNALS
import inspect

i2c = setup_I2C_bus()

def test_screen():        
    my_lcd = SerLCD(bus=i2c)
    my_lcd.clear_screen()
    my_lcd.hello_world()
    my_lcd.contrast(180)

def test_aq_sensor():
    my_aq = SGP30(bus=i2c)
    my_aq.write(MEASURE_RAW_SIGNALS)
    print(my_aq.measure_raw_signals())
    
    
#test_screen()
test_aq_sensor()

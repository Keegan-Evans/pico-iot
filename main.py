from machine import Pin, I2C
from ser_lcd import SerLCD
import utime



i2c = I2C(0, scl=Pin(1, Pin.PULL_UP), sda=Pin(0, Pin.PULL_UP), freq=400000)
utime.sleep_ms(100)
print(i2c.scan())




def test_screen():        
    my_lcd = SerLCD(bus=i2c)
    my_lcd.clear_screen()
    my_lcd.hello_world()
    my_lcd.contrast(180)
    
    
test_screen()
DISPLAY_ADDRESS1 = 0x72 # This is the default address of the OpenLCD
MAX_ROWS = 2
MAX_COLUMNS = 16

# OpenLCD command characters
SPECIAL_COMMAND = 254  # Magic number for sending a special command
SETTING_COMMAND = 0x7C # 124, |, the pipe character: The command to change settings: baud, lines, width, backlight, splash, etc

# OpenLCD commands
CLEAR_COMMAND = 0x2D					# 45, -, the dash character: command to clear and home the display
CONTRAST_COMMAND = 0x18				# Command to change the contrast setting
ADDRESS_COMMAND = 0x19				# Command to change the i2c address
SET_RGB_COMMAND = 0x2B				# 43, +, the plus character: command to set backlight RGB value
ENABLE_SYSTEM_MESSAGE_DISPLAY = 0x2E  # 46, ., command to enable system messages being displayed
DISABLE_SYSTEM_MESSAGE_DISPLAY = 0x2F # 47, /, command to disable system messages being displayed
ENABLE_SPLASH_DISPLAY = 0x30			# 48, 0, command to enable splash screen at power on
DISABLE_SPLASH_DISPLAY = 0x31			# 49, 1, command to disable splash screen at power on
SAVE_CURRENT_DISPLAY_AS_SPLASH = 0x0A # 10, Ctrl+j, command to save current text on display as splash

# special commands
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

import utime
from util import try_until_runs
from machine import Pin

class SerLCD:
    def __init__(self, bus, address=0x72):
        self.address = address
        self.bus = bus
        self.contrast_val = 150
        self._contrast_pin = Pin(15, Pin.IN)
        
    @try_until_runs   
    def write(self, msg):
        if type(msg) ==str:
            msg = msg.encode("utf-8")
        self.bus.writeto(self.address, msg)
    
    @try_until_runs
    def clear_screen(self):
        self.bus.writeto(self.address, bytes([0x7C]))
        self.bus.writeto(self.address, bytes([0x2D]))
        #utime.sleep_ms(10) TODO do these or the try loop thing work better
        
    def contrast(self, contrast):
        self.bus.writeto(self.address, bytearray([0x7C,0x18,contrast]))
        
    def increase_contrast(self):
        self.contrast_val += 5
        self.contrast(self.contrast_val)
            
    @property
    def contrast_pin_state(self):
        return self._contrast_pin.value()

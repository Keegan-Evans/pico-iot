# airquality.py

class SerLCD:
    def __init__(self, bus, address=0x72):
        self.address = address
        self.bus = bus
        self.moisture
        self.calibration_low = 0
        self.calibration_high = 

    def hello_world(self):
        self.bus.writeto(self.address, "hello world")
    
    def clear_screen(self):
        self.bus.writeto(self.address, bytes([0x7C]))
        self.bus.writeto(self.address, bytes([0x2D]))
        
    def high_contrast(self):
        self.bus.writeto(self.address, bytearray([0x7C,0x18,0xB9]))
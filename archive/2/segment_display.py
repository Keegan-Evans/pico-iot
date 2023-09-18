import utime
from machine import Pin, disable_irq

display_pins = [Pin(x, Pin.OUT) for x in [0, 1, 2, 3, 4, 5, 6, 7]]

# 7 segment display pin mappings
# 0x10 is the "off" symbol
display_symbols = {hex(k): [int(x) for x in f'{v:08b}'] for k, v in {
   0x00: 0b00111111,
   0x01: 0b00000011,
   0x02: 0b10101101,
   0x03: 0b10101011,
   0x04: 0b10010011,
   0x05: 0b10111010,
   0x06: 0b10111110,
   0x07: 0b00100011,
   0x08: 0b10111111,
   0x09: 0b10110011,
   0x0A: 0b11110111,
   0x0B: 0b11011110,
   0x0C: 0b01111100,
   0x0D: 0b11001111,
   0x0E: 0b11111100,
   0x0F: 0b11110100,
   0x10: 0b00000000,
}.items()}
#display_symbols = {k: [int(x) for x in f'{v:08b}'] for k, v in display_symbols.items()}
# select which digit to display
# later should behandled by hardware multiplexer
digit_1 = Pin(14, Pin.OUT)
digit_2 = Pin(15, Pin.OUT)

# def display_character(character):
    # if character in display_symbols.keys():
        # pin_vals = display_symbols[character]
        # print(pin_vals)
        # for i, pin in enumerate(display_pins):
            # pin.value(pin_vals[i])

if __name__ == '__main__':
    # for k, v in display_symbols.items():
        # print(hex(k), ":", [int(x) for x in f'{display_symbols[k]:08b}'])
        # utime.sleep(1)

    # print(display_pins)
# 
    # for pin in display_pins:
        # pin.high()
        # utime.sleep(0.5)
        # pin.low()

    # for i in range(15):
        # display_character(i)
        # utime.sleep(1)
    #print(display_symbols)
    
    # while True:
        # digit_1.low()
        # digit_2.high()
        # display_character(0x2)
# 
        # utime.sleep_ms(5)
# 
        # digit_1.high()
        # digit_2.low()
        # display_character(0xb)
# 
        # utime.sleep_ms(5)
# 
    # 
    print(display_symbols)
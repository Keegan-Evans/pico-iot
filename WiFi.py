import network
import secrets
import time

try:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep_ms(100)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    assert wlan.isconnected() == True
except Exception as e:
    raise e

class Networker:
    def __init__(self):
        self._connection = None
    
    def establish_connection(self):
        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            time.sleep_ms(100)
            wlan.connect(secrets.SSID, secrets.PASSWORD)
            assert wlan.isconnected() == True
            self._connection = wlan
        except Exception as e:
            raise e #"Unable to establish wifi connection!"
        
        
    @property
    def connection(self):
        if self._connection is None:
            self.establish_connection()
        return self._connection
        
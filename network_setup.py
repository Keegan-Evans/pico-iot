import network
import secrets
import utime
from util import set_timeout

# try:
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     time.sleep_ms(100)
#     wlan.connect(secrets.SSID, secrets.PASSWORD)
#     assert wlan.isconnected() == True
# except Exception as e:
#     raise e

def connect():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        while 'sensor_hub' not in [x[0].decode('utf-8') for x in wlan.scan()]:
            device_status = 1
            utime.sleep(1)
        
        device_status = 2
        print("Found sensor_hub network")

        device_status = 3

        wlan.connect(secrets.SSID, secrets.PASSWORD)
        while wlan.isconnected() is not True:
            time.sleep(1)
        
        device_status = 4
            
        return wlan
    
    except Exception as e:
        raise e #("Unable to establish wireless network connection.")

# create device status lookup dictionary from device status codes
device_status_lookup = {
    0: "Initializing",
    1: "checking for sensor_hub network",
    2: "Found sensor_hub network",
    3: "connecting to sensor_hub network",
    4: "connected to sensor_hub network"
}



# create a function that takes a network connection and ensures that it is connected
def ensure_connection(wlan):
    if wlan.isconnected() is not True:
        wlan.connect(secrets.SSID, secrets.PASSWORD)
        
        while wlan.isconnected() is not True:
            time.sleep(1)
            
    return wlan
    

# class Networker:
    # def __init__(self):
        # self._connection = None
    # 
    # @set_timeout(10)
    # def establish_connection(self):
        # try:
            # wlan = network.WLAN(network.STA_IF)
            # wlan.active(True)
            # wlan.connect(secrets.SSID, secrets.PASSWORD)
            # 
            # while wlan.isconnected() is not True:
                # time.sleep(1)
                # 
            # return wlan
        # 
        # except Exception as e:
            # raise e #("Unable to establish wireless network connection.")
        # 
        # 
    # @property
    # def connection(self):
        # if self._connection is None:
            # self._connection = self.establish_connection()
        # return self._connection
# 
if __name__ == "__main__":
    print("testing network_setup.py")
    w = connect()
    while True:
        if w.isconnected() == False:
            w = ensure_connection(w)
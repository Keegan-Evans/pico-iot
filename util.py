import network
import rp2
import machine
import utime


# network stuff
rp2.country("US")


def connect_network(max_wait=10):
    """Connect to the network, return the wlan object"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("sensor_hub", "FourCorners")
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print(
            "waiting for connection, current status: {}".format(wlan.status())
        )
        utime.sleep(1)
    print("Connection Established: {}".format(wlan.status()))

    if wlan.status() != 3:
        print("Connection Failed, resetting machine")
        machine.reset()

    return wlan


# other 
def try_until_runs(func):
    def wrapper_try_until_runs(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except OSError as oserr:
                print(oserr)
                continue
            except Exception as e:
                raise e
from machine import Pin, I2C
import utime
#import errno

bus = {'bus_0': (0, 1, 0), 'bus_1': (1, 3, 2)}

def setup_I2C_bus(bus_num='bus_0'):
    i2c = I2C(bus[bus_num][0],
              scl=Pin(bus[bus_num][1],
                      Pin.PULL_UP),
              sda=Pin(bus[bus_num][2],
                      Pin.PULL_UP),
              freq=100000)
    utime.sleep_ms(100)
    print(i2c.scan())
    return i2c


# To be used to repeatedly try I2C operations that can fail with an OSError [errno 5] IO error#
#def try_until_runs(timeout):
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

    return wrapper_try_until_runs

def set_timeout(seconds):
    def timeout_tryer(func):
        def timeout_tryer_wrapper(*args, **kwargs):
            start_time = utime.mktime(utime.gmtime())
            while (utime.mktime(utime.gmtime()) - start_time) < seconds:
                return func(*args, **kwargs)
            raise TimeoutError
        return timeout_tryer_wrapper
    return timeout_tryer


#    return try_until_runs_dec

SUCCESS = 0
FAILURE = 1

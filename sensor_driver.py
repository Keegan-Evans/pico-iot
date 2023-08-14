

class SensorDriver:
    
    # populate init method parameters from current attributes and add default values

    def __init__(self, i2c_bus=None, i2c_address=None, network_connection=None,
                 mqtt_client=None, sensor_pins={}, topic="sensor_data/",
                 sensor_id="sensor", indicator_pin="LED", i2c_command_dict={}, sensor_measurements=[]) -> None:
        # create class attributes for ic2 bus and address, network object, mqtt client, sensor pins, sensor outputs, topic, sensor id, and start time, indicator pin, i2c command dictionary, and sensor variables
        self.i2c_bus = None
        self.i2c_address = None
        self.network_connection = None
        self.mqtt_client = None
        self.sensor_pins = {} # pin: measurement
        self.topic = None
        self.sensor_id = None
        self.start_time = None
        self.indicator_pin = None
        self.i2c_command_dict = None
        self.sensor_measurements = []
        
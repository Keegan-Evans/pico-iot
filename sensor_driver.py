

class SensorDriver:
    
    # populate init method parameters from current attributes and add default values
    # TODO: refactor sensor measurements to be a dictionary of pin: measurement
    def __init__(self, i2c_bus=None, i2c_address=None, network_connection=None,
                 mqtt_client=None, sensor_pins={}, topic="sensor_data/",
                 sensor_id="sensor", indicator_pin="LED", i2c_command_dict={}, sensor_measurements=None) -> None:
        # create class attributes for ic2 bus and address, network object, mqtt client, sensor pins, sensor outputs, topic, sensor id, and start time, indicator pin, i2c command dictionary, and sensor variables
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.network_connection = network_connection
        self.mqtt_client = mqtt_client
        self.sensor_pins = sensor_pins# pin: measurement
        self.topic = topic
        self.sensor_id = sensor_id
        self.indicator_pin = indicator_pin
        self.i2c_command_dict = i2c_command_dict
        self.sensor_measurements = sensor_measurements

        if self.sensor_measurements is not None:
            for each in self.sensor_measurements:
                setattr(self, each, None)
                private_func_name = "_measure_{}".format(each)
                attr_name = "measure_{}".format(each)
                self.attr_name = lambda : self._measure()

    # create method to collect each sensor measurement from self.sensor_measurements and add an attribute to the class for each
    # def collect_sensor_measurements(self):
        # for each in self.sensor_measurements:
            # set attribute for each sensor measurement
            # setattr(self, each, None)
# 
            # self.__dir__().append("measure_{}".format(each))

    def bogus_method(self):
        pass

            
            

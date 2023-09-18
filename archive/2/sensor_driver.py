# sensor_driver.py
# Purpose: SensorDriver class to be used as a base class for all sensor drivers

# for pylance:
# type: ignore

# from tests import test_sensor_driver


class SensorDriver:
    # populate init method parameters from current attributes and add default values
    # TODO: refactor sensor measurements to be a dictionary of pin: measurement
    def __init__(
        self,
        i2c_bus=None,
        i2c_address=None,
        network_connection=None,
        mqtt_client=None,
        sensor_pins={},
        topic="sensor_data/",
        sensor_id="sensor",
        indicator_pin="LED",
        i2c_command_dict={},
        sensor_measurements=None,
        mqtt_broker_address="10.42.0.1",
        SSID="sensor_hub",
        network_password="FourCorners",
    ) -> None:
        # create class attributes for ic2 bus and address, network object, mqtt client, sensor pins, sensor outputs, topic, sensor id, and start time, indicator pin, i2c command dictionary, and sensor variables
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.network_connection = network_connection
        self.mqtt_client = mqtt_client
        self.mqtt_broker_address = mqtt_broker_address
        self.sensor_pins = sensor_pins  # pin: measurement
        self.topic = topic
        self.sensor_id = sensor_id
        self.indicator_pin = indicator_pin
        self.i2c_command_dict = i2c_command_dict
        self.sensor_measurements = sensor_measurements
        self.SSID = SSID
        self.PASSWORD = network_password

        # TODO: enable logging, display, or transmission of exceptions
        self.most_recent_exception = None

        # TODO: TEST status_codes
        self.status_codes = {
            ("network", "connection_established"): bytearray([0x01, 0x00]),
            ("network", "not_connected_target_network_not_found"): bytearray(
                [0x01, 0x01]
            ),
            ("network", "not_connected_waiting"): bytearray([0x01, 0x02]),
            ("mqtt", "connection_error"): bytearray([0x04, 0x01]),
            ("mqtt", "connection_error_broker_unreachable"): bytearray(
                [0x04, 0x02]
            ),
            ("mqtt", "connection_error_network_error"): bytearray(
                [0x04, 0x03]
            ),
            ("mqtt", "connection_established"): bytearray([0x04, 0x00]),
        }

        # TODO: create measure function for each sensor measurement
        # TODO: needs to be implemented as ABC?
        # if self.sensor_measurements is not None:
        # for each in self.sensor_measurements:
        # setattr(self, each, None)
        # private_func_name = "_measure_{}".format(each)
        # attr_name = "measure_{}".format(each)
        # self.attr_name = lambda : self._measure()

    def bogus_method(self):
        pass

    # TODO: add sensor_status attribute to SensorDriver class
    # TODO: implement method to emit sensor status code to 7 segment display
    # TODO: implement 7 segment display class
    # TODO: implement method to create and register appropriate database tables

    def _establish_network_connection(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if self.SSID not in [
            found_network[0].decode() for found_network in wlan.scan()
        ]:
            self.sensor_status = self.status_codes[
                ("network", "not_connected_target_network_not_found")
            ]
            return None

        wlan.connect(self.SSID, self.PASSWORD)

        while not wlan.isconnected():
            self.sensor_status = self.status_codes[
                ("network", "not_connected_waiting")
            ]
            utime.sleep(1)

        self.network_connection = wlan
        self.sensor_status = self.status_codes[
            ("network", "connection_established")
        ]

    def _establish_mqtt_connection(self):
        if self.network_connection is None:
            self._establish_network_connection()
        try:
            client = MQTTClient(
                self.sensor_id,
                self.mqtt_broker_address,
                port=1883,
                keepalive=3,
            )
            client.connect()
            self.sensor_status = self.status_codes[
                ("mqtt", "connection_established")
            ]
            self.mqtt_client = client
            return None
        except OSError as e:
            self.most_recent_exception = e
            if e.args[0] == -2:
                print("Unable to connect to MQTT broker, unreachable")
                self.sensor_status = self.status_codes[
                    ("mqtt", "connection_error_broker_unreachable")
                ]
            else:
                print("Unable to connect to MQTT broker: {}".format(e.args[0]))
                self.sensor_status = self.status_codes[
                    ("mqtt", "connection_error")
                ]
            return None
        except Exception as e:
            self.most_recent_exception = e
            self.sensor_status = self.status_codes[
                ("mqtt", "connection_error")
            ]
            return None


if __name__ == "__main__":
    # tests to be moved to own file after development
    def test_instantiation():
        sensor_driver = SensorDriver()
        assert isinstance(sensor_driver, SensorDriver)

    def test_default_class_attributes():
        sensor_driver = SensorDriver()

        expected_attributes = [
            "i2c_bus",
            "i2c_address",
            "network_connection",
            "mqtt_client",
            "sensor_pins",
            "topic",
            "sensor_id",
            "indicator_pin",
            "i2c_command_dict",
            "sensor_measurements",
        ]

        for attribute in expected_attributes:
            try:
                assert hasattr(sensor_driver, attribute)
            except AssertionError:
                print(f"Attribute {attribute} not found in SensorDriver class")
                raise AssertionError

    # TODO: finish method to create measurement methods
    def test_create_measurement_methods():
        test_driver = SensorDriver(
            sensor_measurements=[
                "temperature",
                "humidity",
                "pressure",
                "altitude",
            ]
        )
        print(test_driver.__dict__)
        # print(inspect.getmembers(test_driver))

    def test_establish_network_connection():
        test_driver = SensorDriver()
        test_driver._establish_network_connection()

        assert (
            test_driver.sensor_status
            == test_driver.status_codes[("network", "connection_established")]
        )

    def test_establish_network_connection_target_network_not_found():
        test_driver = SensorDriver(SSID="bogus_network")
        test_driver._establish_network_connection()

        assert (
            test_driver.sensor_status
            == test_driver.status_codes[
                ("network", "not_connected_target_network_not_found")
            ]
        )

    def test_establish_mqtt_connection_good():
        test_driver = SensorDriver()
        test_driver._establish_mqtt_connection()

        assert (
            test_driver.sensor_status
            == test_driver.status_codes[("mqtt", "connection_established")]
        )

    def test_establish_mqtt_connection_error():
        test_driver = SensorDriver(mqtt_broker_address="bogus_broker_address")
        test_driver._establish_mqtt_connection()

        assert (
            test_driver.sensor_status
            == test_driver.status_codes[
                ("mqtt", "connection_error_broker_unreachable")
            ]
        )

    def test_mqtt_handler_establishes_network_connection():
        test_sensor_driver = SensorDriver()
        assert test_sensor_driver.network_connection is None

        test_sensor_driver._establish_mqtt_connection()
        assert test_sensor_driver.network_connection is not None

    # test_instantiation()
    # test_default_class_attributes()
    # test_create_measurement_methods()
    # print('test: establish_network_connection')
    # test_establish_network_connection()
#
# print('test: establish_network_connection_target_network_not_found')
# test_establish_network_connection_target_network_not_found()
#
# print('test: establish_mqtt_connection_good')
# test_establish_mqtt_connection_good()
#
# print('test: establish_mqtt_connection_error')
# test_establish_mqtt_connection_error()

# print('test: mqtt_handler_establishes_network_connection')
# test_mqtt_handler_establishes_network_connection()

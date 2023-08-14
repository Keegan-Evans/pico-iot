from sensor_driver import SensorDriver

def test_instantiation():
    sensor_driver = SensorDriver()
    assert isinstance(sensor_driver, SensorDriver)

def test_default_class_attributes():
    sensor_driver = SensorDriver()

    expected_attributes = ['i2c_bus', 'i2c_address', 'network_connection', 'mqtt_client', 'sensor_pins', 'topic', 'sensor_id', 'start_time', 'indicator_pin',
    'i2c_command_dict', 'sensor_measurements']

    for attribute in expected_attributes:
        try:
            assert hasattr(sensor_driver, attribute)
        except AssertionError:
            print(f"Attribute {attribute} not found in SensorDriver class")
            raise AssertionError

if __name__ == '__main__':
    test_instantiation()
    test_default_class_attributes()
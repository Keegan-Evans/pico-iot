from sensor_driver import SensorDriver
#import inspect

def test_instantiation():
    sensor_driver = SensorDriver()
    assert isinstance(sensor_driver, SensorDriver)

def test_default_class_attributes():
    sensor_driver = SensorDriver()

    expected_attributes = ['i2c_bus', 'i2c_address', 'network_connection', 'mqtt_client', 'sensor_pins', 'topic', 'sensor_id', 'indicator_pin',
    'i2c_command_dict', 'sensor_measurements']

    for attribute in expected_attributes:
        try:
            assert hasattr(sensor_driver, attribute)
        except AssertionError:
            print(f"Attribute {attribute} not found in SensorDriver class")
            raise AssertionError

# TODO: finish method to create measurement methods
def test_create_measurement_methods():
    test_driver = SensorDriver(sensor_measurements = ['temperature', 'humidity', 'pressure', 'altitude'])
    print(test_driver.__dict__)
    #print(inspect.getmembers(test_driver))

def test_establish_network_connection():
    test_driver = SensorDriver()
    test_driver._establish_network_connection()
    
    assert test_driver.sensor_status == test_driver.status_codes[('network', 'connection_established')]

def test_establish_network_connection_target_network_not_found():
    test_driver = SensorDriver(SSID = 'bogus_network')
    test_driver._establish_network_connection()
    
    assert test_driver.sensor_status == test_driver.status_codes[('network', 'not_connected_target_network_not_found')]
    
def test_establish_mqtt_connection():
    test_driver = SensorDriver()
    test_driver._establish_network_connection()
    test_driver._establish_mqtt_connection()

    assert test_driver.sensor_status == test_driver.status_codes[('mqtt', 'connection_established')]



if __name__ == '__main__':
    #test_instantiation()
    #test_default_class_attributes()
    #test_create_measurement_methods()
    print('testing_establish_network_connection')
    test_establish_network_connection()
    print('establish_network_connection_target_network_not_found')
    test_establish_network_connection_target_network_not_found()
    print('test_establish_mqtt_connection')
    test_establish_mqtt_connection()


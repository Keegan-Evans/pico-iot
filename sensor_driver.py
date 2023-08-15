# sensor_driver.py
# Purpose: SensorDriver class to be used as a base class for all sensor drivers

# for pylance:
# type: ignore

from umqtt_simple import MQTTClient
import network

class SensorDriver:
    
    # populate init method parameters from current attributes and add default values
    # TODO: refactor sensor measurements to be a dictionary of pin: measurement
    def __init__(self, i2c_bus=None, i2c_address=None, network_connection=None,
                 mqtt_client=None, sensor_pins={}, topic="sensor_data/",
                 sensor_id="sensor", indicator_pin="LED", i2c_command_dict={}, sensor_measurements=None,
                 mqtt_broker_address='10.42.0.1', SSID='sensor_hub', network_password='FourCorners',
                 )-> None:
        # create class attributes for ic2 bus and address, network object, mqtt client, sensor pins, sensor outputs, topic, sensor id, and start time, indicator pin, i2c command dictionary, and sensor variables
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.network_connection = network_connection
        self.mqtt_client = mqtt_client
        self.mqtt_broker_address = mqtt_broker_address
        self.sensor_pins = sensor_pins# pin: measurement
        self.topic = topic
        self.sensor_id = sensor_id
        self.indicator_pin = indicator_pin
        self.i2c_command_dict = i2c_command_dict
        self.sensor_measurements = sensor_measurements
        self.SSID = SSID
        self.PASSWORD = network_password

        # TODO: TEST status_codes
        self.status_codes = {
            ('network', 'connection_established'): bytearray([0x01, 0x00]),
            ('network', 'not_connected_target_network_not_found'): bytearray([0x01, 0x01]),
            ('network', 'not_connected_waiting'): bytearray([0x01, 0x02]),
            ('mqtt', 'connection_error'): bytearray([0x04, 0x01]),
            ('mqtt', 'connection_error_broker_unreachable'): bytearray([0x04, 0x02]),
            ('mqtt', 'connection_error_network_error'): bytearray([0x04, 0x03]),
            ('mqtt', 'connection_established'): bytearray([0x04, 0x00]),
            }


        # TODO: create measure function for each sensor measurement
        # TODO: needs to be implemented as ABC?
        # if self.sensor_measurements is not None:
            # for each in self.sensor_measurements:
                # setattr(self, each, None)
                # private_func_name = "_measure_{}".format(each)
                # attr_name = "measure_{}".format(each)
                #self.attr_name = lambda : self._measure()

    def bogus_method(self):
        pass

    # TODO: add sensor_status attribute to SensorDriver class
    # TODO: implement method to emit sensor status code to 7 segment display
    # TODO: implement 7 segment display class
    # TODO: implement method to create and register appropriate database tables

    # TODO: TEST method to intialize network connection
    def _establish_network_connection(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if self.SSID not in [found_network[0].decode() for found_network in wlan.scan()]:
            self.sensor_status = self.status_codes[('network', 'not_connected_target_network_not_found')]
            break


        wlan.connect(self.SSID, self.PASSWORD)

        while not wlan.isconnected():
           self.sensor_status = self.status_codes[('network', 'not_connected_waiting')]

        self.network_connection = wlan
        self.sensor_status = self.status_codes[('network', 'connection_established')]



    # TODO: TEST method to intialize MQTT connection
    # test good
    # test no network connection
    # test broker unreachable
    def _establish_mqtt_connection(self):
        try:
            client = MQTTClient(self.sensor_id, self.mqtt_broker_address, port=1883, keepalive=15)
            self.mqtt_client = client
            self.sensor_status = self.status_codes[('mqtt', 'connection_established')]
        except Exception as e:
            self.sensor_status = self.status_codes[('mqtt', 'unable_to_establish_connection')]
            raise e
            

            
            

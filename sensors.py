class Sensor:
    def __init__(self, i2c_bus, mqtt_handler, topic="sensor", sensor_id="default-sensor-id", indicator_pin="LED"):
        self.mqtt_handler = mqtt_handler
        self.topic = topic
        self.sensor_id = sensor_id

    # I2C methods
    # Methods that interact with the bus directly need to use
    # @try_until_runs and @set_timeout decorators

    # for use when checksums required
    def create_message_packet(self, msg):
        return msg + self.create_checksum(msg)

    @set_timeout(10)
    @try_until_runs
    def write_i2c(self, msg):
        self.bus.writeto(self.i2c_address, create_message_packet(msg))

    # ADC methods

    # MQTT methods
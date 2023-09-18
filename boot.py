from util import connect_network
from mqtt import MQTTClient
from sensor import AnalogSensor, Sensor

wlan = connect_network()
client = MQTTClient("test_bed", "10.42.0.1")

sm_probe = AnalogSensor(pin=28, name="sm_probe")

sm = Sensor(
    topic="sensor_data",
    sensor_id="test_rig1",
    mqtt_handler=client,
    measurements=[sm_probe],
)

if __name__ == "__main__":
    print(wlan.status())
    print(client)

    sm.publish()

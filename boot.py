from util import connect_network
from mqtt import MQTTClient
from sensor import AnalogSensor, Sensor
from weather_station import WeatherStation


wlan = connect_network()
client = MQTTClient("weather_station_tester", "10.42.0.1")

sm_probe = AnalogSensor(pin=28, name="sm_probe")

sm = Sensor(
    topic="sensor_data",
    sensor_id="test_rig1",
    mqtt_handler=client,
    measurements=[sm_probe],
)

ws = WeatherStation(
    topic="sensor_data/weather",
    sensor_id="weather_station_1",
    mqtt_handler=client,
)

if __name__ == "__main__":
    print(wlan.status())
    print(client)
    ws.begin()

    while True:
        ws.publish()

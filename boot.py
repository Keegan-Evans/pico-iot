from util import connect_network
from mqtt import MQTTClient
from weather_station import WeatherStation


wlan = connect_network()


SENSOR_ID = "weather_station_demo_1"
BROKER_ADDR = "10.42.0.1"

client = MQTTClient(SENSOR_ID, BROKER_ADDR, port=1883, keepalive=10)

ws = WeatherStation(
    topic="sensor_data/weather",
    mqtt_handler=client,
)


# test the wind speed funtions


if __name__ == "__main__":
    ws.begin()

    while True:
        ws.publish()

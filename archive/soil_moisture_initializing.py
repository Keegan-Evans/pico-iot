sm_probe = AnalogSensor(pin=28, name="sm_probe")

sm = Sensor(
    topic="sensor_data",
    sensor_id="test_rig1",
    mqtt_handler=client,
    measurements=[sm_probe],
)

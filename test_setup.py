def setup_for_testing():
    from network_setup import Networker
    from umqtt.simple import MQTTClient
    
    print("imports")
    wlan = Networker().establish_connection()
    print("wifi connection established")
    
    client = MQTTClient('sense_board_1', '192.168.1.14', port=1883, keepalive=60)
    print("mqtt broker connection established")
    return wlan, client
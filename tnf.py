from network import WLAN, STA_IF
import network

wlan = WLAN(STA_IF)
wlan.active(True)
wlan.connect("ChillCottage", "WelcomeToTheInternet")
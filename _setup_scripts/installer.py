from ..util import Networker
import mip

# setup network
wlan = Networker().establish_connection()

# mqtt install
mip.install('umqtt.simple')
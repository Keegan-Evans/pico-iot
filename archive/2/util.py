import network
import utime
import rp2
import machine
import secrets
import time
from machine import Pin, I2C

import usocket as socket
import ustruct as struct
from ubinascii import hexlify

# network connection utility function
rp2.country("US")


def connect_network(max_wait=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("sensor_hub", "FourCorners")
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print(
            "waiting for connection, current status: {}".format(wlan.status())
        )
        utime.sleep(1)
    print("Connection Established: {}".format(wlan.status()))

    if wlan.status() != 3:
        print("Connection Failed, resetting machine")
        machine.reset()

    return wlan


###############################################################################
# Header Like
###############################################################################

SUCCESS = 0
FAILURE = 1


###############################################################################
# Util Functions
###############################################################################


def crc8(data, table, poly=0x31, init_value=0xFF, final_xor=0x00):
    crc = init_value

    for byte in data:
        crc ^= byte
        crc = int.from_bytes(table[crc], "big")
        return bytes([crc ^ final_xor])


def create_message_packet(data):
    byte_data = b""

    if data is str:
        byte_data += data.encode("utf-8")

    elif data is int:
        byte_data += str(data).encode("utf-8")

    elif data is bytes or bytearray:
        byte_data += data

    else:
        raise ValueError(
            "Type of the provided data({}) does not match str, bytes, "
            "bytearray".format(data.type)
        )

    byte_data += crc8(byte_data, SGP30_LOOKUP)

    return byte_data


# def add_checksum(msg):
#     with len(msg) as msg_length::w

#         if msg_length % 2 != 0:
#             raise ValueError("Detected an odd number of bytes{} in message, "
#                              "but expected an even number"
#             )


def generate_crc_table(poly):
    # Generate CRC lookup table
    table = [str(0).encode()] * 256
    print(type(table))
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFF

        table.insert(i, str(crc).encode("utf-8"))

    return table


SGP30_LOOKUP = generate_crc_table(0x31)


def try_until_runs(func):
    def wrapper_try_until_runs(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except OSError as oserr:
                print(oserr)
                continue
            except Exception as e:
                raise e

    return wrapper_try_until_runs


def set_timeout(seconds):
    def timeout_tryer(func):
        def timeout_tryer_wrapper(*args, **kwargs):
            start_time = utime.mktime(utime.gmtime())
            while (utime.mktime(utime.gmtime()) - start_time) < seconds:
                return func(*args, **kwargs)
            raise TimeoutError

        return timeout_tryer_wrapper

    return timeout_tryer


###############################################################################
# Setup I2C bus
###############################################################################


I2C_bus_pin_mapper = {"bus_0": (0, 1, 0), "bus_1": (1, 3, 2)}


def I2C_pin_mapper(bus_num="bus_0"):
    return I2C_bus_pin_mapper[bus_num]


def setup_I2C_bus(bus_num="bus_0"):
    pin_map = I2C_pin_mapper(bus_num)
    i2c = I2C(
        pin_map[0],
        scl=Pin(pin_map[1], Pin.PULL_UP),
        sda=Pin(pin_map[2], Pin.PULL_UP),
        freq=100000,
    )
    utime.sleep_ms(100)
    print(i2c.scan())
    return i2c, pin_map[0]


###############################################################################
# Wifi Connection
###############################################################################


###############################################################################
# Seven Segment Display Driver
###############################################################################


class SevenSegmentDisplay:
    def __init__(self, dot_pin, segment_pin_list):
        self.dot_pin = Pin(dot_pin, Pin.OUT)
        self.segment_pin_list = segment_pin_list
        self.pins = {}

        for idx, pin_num in enumerate(segment_pin_list):
            self.pins[pin_num] = Pin(pin_num, Pin.OUT)

    def display_value(self, value):
        char_table = {
            "0": [1, 1, 1, 1, 1, 1, 0],
            "1": [0, 1, 1, 0, 0, 0, 0],
            "2": [1, 1, 0, 1, 1, 0, 1],
            "3": [1, 1, 1, 1, 0, 0, 1],
            "4": [0, 1, 1, 0, 0, 1, 1],
            "5": [1, 0, 1, 1, 0, 1, 1],
            "6": [1, 0, 1, 1, 1, 1, 1],
            "7": [1, 1, 1, 0, 0, 0, 0],
            "8": [1, 1, 1, 1, 1, 1, 1],
            "9": [1, 1, 1, 1, 0, 1, 1],
            "A": [1, 1, 1, 0, 1, 1, 1],
            "B": [0, 0, 1, 1, 1, 1, 1],
            "C": [1, 0, 0, 1, 1, 1, 0],
            "D": [0, 1, 1, 1, 1, 0, 1],
            "E": [1, 0, 0, 1, 1, 1, 1],
            "F": [1, 0, 0, 0, 1, 1, 1],
        }

        for idx, val in enumerate(char_table[value]):
            self.pins[self.segment_pin_list[idx]] = val


# define function to establish network connection


# define function to establish MQTT connection
class MQTTException(Exception):
    pass


class MQTTClient:
    def __init__(
        self,
        client_id,
        server,
        port=0,
        user=None,
        password=None,
        keepalive=0,
        ssl=False,
        ssl_params={},
    ):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.sock = None
        self.server = server
        self.port = port
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False

    def _send_str(self, s):
        self.sock.write(struct.pack("!H", len(s)))
        self.sock.write(s)

    def _recv_len(self):
        n = 0
        sh = 0
        while 1:
            b = self.sock.read(1)[0]
            n |= (b & 0x7F) << sh
            if not b & 0x80:
                return n
            sh += 7

    def set_callback(self, f):
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True):
        self.sock = socket.socket()
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]
        self.sock.connect(addr)
        if self.ssl:
            import ussl

            self.sock = ussl.wrap_socket(self.sock, **self.ssl_params)
        premsg = bytearray(b"\x10\0\0\0\0\0")
        msg = bytearray(b"\x04MQTT\x04\x02\0\0")

        sz = 10 + 2 + len(self.client_id)
        msg[6] = clean_session << 1
        if self.user is not None:
            sz += 2 + len(self.user) + 2 + len(self.pswd)
            msg[6] |= 0xC0
        if self.keepalive:
            assert self.keepalive < 65536
            msg[7] |= self.keepalive >> 8
            msg[8] |= self.keepalive & 0x00FF
        if self.lw_topic:
            sz += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)
            msg[6] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
            msg[6] |= self.lw_retain << 5

        i = 1
        while sz > 0x7F:
            premsg[i] = (sz & 0x7F) | 0x80
            sz >>= 7
            i += 1
        premsg[i] = sz

        self.sock.write(premsg, i + 2)
        self.sock.write(msg)
        # print(hex(len(msg)), hexlify(msg, ":"))
        self._send_str(self.client_id)
        if self.lw_topic:
            self._send_str(self.lw_topic)
            self._send_str(self.lw_msg)
        if self.user is not None:
            self._send_str(self.user)
            self._send_str(self.pswd)
        resp = self.sock.read(4)
        assert resp[0] == 0x20 and resp[1] == 0x02
        if resp[3] != 0:
            raise MQTTException(resp[3])
        return resp[2] & 1

    def disconnect(self):
        self.sock.write(b"\xe0\0")
        self.sock.close()

    def ping(self):
        self.sock.write(b"\xc0\0")

    def publish(self, topic, msg, retain=False, qos=0):
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2
        assert sz < 2097152
        i = 1
        while sz > 0x7F:
            pkt[i] = (sz & 0x7F) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        # print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt, i + 1)
        self._send_str(topic)
        if qos > 0:
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.write(pkt, 2)
        self.sock.write(msg)
        if qos == 1:
            while 1:
                op = self.wait_msg()
                if op == 0x40:
                    sz = self.sock.read(1)
                    assert sz == b"\x02"
                    rcv_pid = self.sock.read(2)
                    rcv_pid = rcv_pid[0] << 8 | rcv_pid[1]
                    if pid == rcv_pid:
                        return
        elif qos == 2:
            assert 0

    def subscribe(self, topic, qos=0):
        assert self.cb is not None, "Subscribe callback is not set"
        pkt = bytearray(b"\x82\0\0\0")
        self.pid += 1
        struct.pack_into("!BH", pkt, 1, 2 + 2 + len(topic) + 1, self.pid)
        # print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt)
        self._send_str(topic)
        self.sock.write(qos.to_bytes(1, "little"))
        while 1:
            op = self.wait_msg()
            if op == 0x90:
                resp = self.sock.read(4)
                # print(resp)
                assert resp[1] == pkt[2] and resp[2] == pkt[3]
                if resp[3] == 0x80:
                    raise MQTTException(resp[3])
                return

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def wait_msg(self):
        res = self.sock.read(1)
        self.sock.setblocking(True)
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)
        if res == b"\xd0":  # PINGRESP
            sz = self.sock.read(1)[0]
            assert sz == 0
            return None
        op = res[0]
        if op & 0xF0 != 0x30:
            return op
        sz = self._recv_len()
        topic_len = self.sock.read(2)
        topic_len = (topic_len[0] << 8) | topic_len[1]
        topic = self.sock.read(topic_len)
        sz -= topic_len + 2
        if op & 6:
            pid = self.sock.read(2)
            pid = pid[0] << 8 | pid[1]
            sz -= 2
        msg = self.sock.read(sz)
        self.cb(topic, msg)
        if op & 6 == 2:
            pkt = bytearray(b"\x40\x02\0\0")
            struct.pack_into("!H", pkt, 2, pid)
            self.sock.write(pkt)
        elif op & 6 == 4:
            assert 0
        return op

    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def check_msg(self):
        self.sock.setblocking(False)
        return self.wait_msg()

# json_wrapper.py

import json

data_vals = bytearray([0x05, 0xA3, 0xFE])

data_dict = {'data thing0': int.from_bytes(data_vals[0:2], 'big'),
             'data_thing1': int(data_vals[2]),
             'data_thing2': 'A thing you can enjoy'}

print(data_dict)

encoded_data_obj = json.dumps(data_dict)
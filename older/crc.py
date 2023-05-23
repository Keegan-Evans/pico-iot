def crc8(data, table, poly=0x31, init_value=0xFF, final_xor=0x00):
    crc = init_value

    for byte in data:
        crc ^= byte
        crc = int.from_bytes(table[crc], 'big')

    return bytes([crc ^ final_xor])

def create_message_packet(data):
    byte_data = b''
 
    if type(data) == str:
        byte_data += data.encode("utf-8")
    
    elif type(data) == int:
        byte_data += str(data).encode("utf-8")


    elif type(data) == bytes or bytearray:
        byte_data += data
        
    else:
        raise ValueError("Type of the provided data({}) does not match str, bytes, bytearray".format(data.type))
        
    byte_data += crc8(byte_data, SGP30_LOOKUP)
    return byte_data
    
# def add_checksum(msg):
#     with len(msg) as msg_length::w

#         if msg_length % 2 != 0:
#             raise ValueError("Detected an odd number of bytes{} in message, but expected an even number")
#         for

def generate_crc_table(poly):
    # Generate CRC lookup table
    table = [0] * 256
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFF
        table[i] = crc.to_bytes(1, 'big')
    return table

SGP30_LOOKUP = generate_crc_table(0x31)

#test_buf = 0xBEEF.to_bytes(2, 'big')
##test
#assert crc8(test_buf,SGP30_lookup) == 0x92

if __name__ == '__main__':
    d_a = bytes([0xbe, 0xef])
    d_b = bytearray([0xbe, 0xef])
    d_c = 'the fat, smelly cat'
    d_d = 975186
    
    c_a = crc8(d_a, SGP30_LOOKUP)
    r_a = create_message_packet(d_a)

    print(len(r_a), r_a)
    
    r_b = create_message_packet(d_b)
    print(len(r_b), r_b)
    
    r_c = create_message_packet(d_c)
    print(len(r_c), r_c)
    
    r_d = create_message_packet(d_d)
    print(len(r_d), r_d)
    

    
    
    
from binascii import b2a_hex
with open('rawdata.txt', 'rb') as file:
    data = file.read()
    data = b2a_hex(data)
    print(data)

from binascii import a2b_hex

with open('t.txt', 'r') as read:
    readdata = read.readlines()
    print(readdata)
    readdata = readdata[0]
    readdata = str(readdata)
    readdata.replace('\'', '')
    print(readdata)
    with open('fff2.txt', 'a') as inp:
        print(type(readdata))
        print(a2b_hex(readdata))
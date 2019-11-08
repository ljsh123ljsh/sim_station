import asyncio
from base64 import b64encode
from binascii import b2a_hex
from redis import StrictRedis
import socket


async def loadtoredis(content, mp, r):
    r.lpush(mp, content)


def creat(sourcepoint):
    ip = '192.168.130.28'  # 连接服务器IP
    port = 8107  # 连接服务器端口
    pwd = 'cmcc'  # 登录密码
    user = 'cmcc'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接
    s.connect((ip, port))
    EncryptionStr = b64encode(str.encode(user + ":" + pwd))
    # 发送登录包
    SendMsg = "POST /" + sourcepoint + " HTTP/1.1\r\nHost: 172.16.31.235:15656\r\nNtrip-Version: Ntrip/2.0\r\nUser-Agent: NTRIP Hi-Target-iRTK\r\nAuthorization: Basic " + bytes.decode(
        EncryptionStr) + "\r\nNtrip-STR:\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n"
    print(SendMsg)
    s.sendall(str.encode(SendMsg))
    ReturnResult = s.recv(4096)
    return s, ReturnResult

async def postdata(s, res, data):
    if "ICY 200 OK" == bytes.decode(res[0:10]):
        while True:
            s.sendall(data)
            await asyncio.sleep(1)

async def get(mountpoint, r):
    ip = '192.168.130.28'  # 连接服务器IP
    port = 8107  # 连接服务器端口
    user = 'cmcc'  # 登录用户
    pwd = 'cmcc'  # 登录密码
    connect = asyncio.open_connection(host=ip, port=port)
    reader, writer = await connect

    EncryptionStr = b64encode(str.encode(user + ":" + pwd))
    # 发送登录包
    SendMsg = "GET /" + mountpoint + " HTTP/1.1\r\nHost: 172.16.31.235:15656\r\nNtrip-Version: Ntrip/2.0\r\nUser-Agent: NTRIP Hi-Target-iRTK\r\nAuthorization: Basic " + bytes.decode(
        EncryptionStr) + "\r\nNtrip-STR:\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n"
    SendMsg = SendMsg.encode()
    writer.write(SendMsg)
    await writer.drain()
    ok = await reader.readline()
    if ok == b'ICY 200 OK\r\n' :
        s, ret = creat('1002008001')
        # while 1:
        #     res = await reader.read(3000)
        #     # res = await reader.readline()
        #     # res = b2a_hex(res)
        #     # with open('rawdata.txt', 'rb') as file :
        #     #     res = file.read()
        #     await postdata(s, ret, res)
        #     print(res)
        #     await loadtoredis(res, mountpoint, r)

        res = await reader.read(3000)
        await postdata(s, ret, res)
        print(res)
        await loadtoredis(res, mountpoint, r)







def main():
    r = StrictRedis(host='49.233.166.39', port=6379, db=14)
    # mp_li = ['SHJQ', 'SHBN', 'SHYL', 'SHTP', 'SHMY', 'SHSQ', 'SHSL', 'SHJQ', 'SHFX', 'SHLG']
    mp_li = ['SHJQ']
    task = [get(mp, r) for mp in mp_li]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))
if __name__ == '__main__':
    main()




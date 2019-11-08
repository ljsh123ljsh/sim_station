import socket
from base64 import b64encode
import asyncio
import GetData

def CreateTCPScoket(sourcepoint,user):
    ip = '192.168.130.28'  # 连接服务器IP
    port = 8107  # 连接服务器端口
    pwd = 'cmcc'  # 登录密码
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接
    s.connect((ip, port))
    EncryptionStr = b64encode(str.encode(user + ":" + pwd))
    #发送登录包
    SendMsg = "POST /"+sourcepoint+" HTTP/1.1\r\nHost: 172.16.31.235:15656\r\nNtrip-Version: Ntrip/2.0\r\nUser-Agent: NTRIP Hi-Target-iRTK\r\nAuthorization: Basic "+bytes.decode(EncryptionStr)+"\r\nNtrip-STR:\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n"
    print(SendMsg)
    s.sendall(str.encode(SendMsg))
    ReturnResult = s.recv(4096)
    return s, ReturnResult

def main():
    s, r = CreateTCPScoket('1002008001', 'cmcc')
    if "ICY 200 OK" == bytes.decode(r[0:10]):
        while 1:
            data = GetData.main()


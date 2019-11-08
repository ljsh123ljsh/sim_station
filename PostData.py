# -*- coding: utf-8 -*-
#!user/bin/python
#模拟ntrip2.0协议基站用户并发


import socket,threading,time,base64
threads = []
threadlock = threading.Lock()

concurrencyNum = 1   #并发用户数
class MyTread(threading.Thread):
    print("start time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    def __init__(self,sourcepoint,user):
        threading.Thread.__init__(self)
        self.sourcepoint = sourcepoint
        self.user = user
        self.Socket = ""
        self.ReturnResult = ""

    def run(self):
        while 1:
            # threadlock.acquire()
            self.Socket, self.ReturnResult = CreateTCPScoket(self.sourcepoint, self.user)
            # threadlock.release()
            if "ICY 200 OK" == bytes.decode(self.ReturnResult[0:10]):
                while True:
                    #发送3kb原始数据
                    data = ReadServerData()
                    self.Socket.sendall(data)
                    time.sleep(1)
            else:
                print("Error:返回值为"+bytes.decode(self.ReturnResult))
            self.Socket.close()

def CreateTCPScoket(sourcepoint,user):
    ip = '192.168.130.28'  # 连接服务器IP
    port = 8107  # 连接服务器端口
    pwd = 'cmcc'  # 登录密码
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接
    s.connect((ip, port))
    EncryptionStr = base64.b64encode(str.encode(user + ":" + pwd))
    #发送登录包
    SendMsg = "POST /"+sourcepoint+" HTTP/1.1\r\nHost: 172.16.31.235:15656\r\nNtrip-Version: Ntrip/2.0\r\nUser-Agent: NTRIP Hi-Target-iRTK\r\nAuthorization: Basic "+bytes.decode(EncryptionStr)+"\r\nNtrip-STR:\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n"
    print(SendMsg)
    s.sendall(str.encode(SendMsg))
    ReturnResult = s.recv(4096)
    return s, ReturnResult

def ReadServerData():
    file = open("rawdata.txt", "rb")
    data = file.read()
    file.close()
    return data

for t in range(0,concurrencyNum):
    i0 = 1002008001
    i1 = 40011000
    sourcepoint = str(t+i0)
    user = str(t+i1)
    Thread = MyTread(sourcepoint, user)
    Thread.start()
    threads.append(Thread)

for thread in threads:
    thread.join()

print("end time:" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
'''
#基准站发送登录数据包
POST /9020008014 HTTP/1.1
Host: 202.96.185.34:65000
Ntrip-Version: Ntrip/2.0
User-Agent: NTRIP Hi-Target-iRTK
Authorization: Basic MTAwMTI3Mzk6emhkZ3Bz
Ntrip-STR:
Connection: close
Transfer-Encoding: chunked\r\n
'''

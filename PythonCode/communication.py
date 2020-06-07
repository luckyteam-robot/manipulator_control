#######  tcp通讯协议程序，使PC机与大机械臂“织女”进行信息收发通讯   ########
from socket import *
import time
from numpy import *
def tcptransmit(Pobj):
    """
    tcp发送程序函数
    :param Pobj:
    :return:
    """
    server = socket()
    server.bind(('192.168.1.101',8080))
    server.listen()
    conn,client_addr = server.accept()
    Pb0obj = Pobj
    x = Pb0obj[0,0]
    y = Pb0obj[1,0]
    z = Pb0obj[2,0]
    p = 50
    w = 60
    r = 90
    xstr = "x:" + str(x)
    ystr = "y:" + str(y)
    zstr = "z:" + str(z)
    wstr = "w:" + str(w)
    pstr = "y:" + str(p)
    rstr = "z:" + str(r)
    str1 = xstr + "," + ystr+","+zstr+","+wstr+","+pstr+","+rstr
    data = str1.encode()
    conn.send(data)
    print("发送")
    print(Pobj)
tcptransmit(mat([1,2,]
                ))
def tcprecieve():
    """
    tcp通讯接受函数
    :return: pc机接受到的字符串
    """
    time.sleep(0.5)
    client = socket()
    client.connect(('192.168.1.100', 8080))
    data = client.recv(1024)
    print("output", data)
    return data






#写一个USB串行通信的程序，使得PC机可与stm32进行信息通信
#尚待补充，编写相应的通信收发程序
import serial
import serial.tools.list_ports

#查找是否有串口存在
def findcom():
    """
    查找串口的函数程序
    :return: 所有打开的串口
    """
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print("无可用串口！")
    else:
        for i in range(0, len(port_list)):
            print(port_list[i])

    return port_list

def usbtransmit(String,port):
    """
    通信发送函数
    通信协议，结尾应加上0D 0A的16进制（表示数据发送完成）
    发送16进制数：利用chr（0x0d）来发送
    例如：usbtransmit(chr(0x3c),"COM1") 表示从com1口发送16进制数0x3c
    :param String:
    :return:
    """
    try:
        # 端口：CNU； Linux上的/dev /ttyUSB0等； windows上的COM3等
        portx ="COM1" #port  #"COM1"

        # 波特率，标准值有：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        bps = 115200

        # 超时设置，None：永远等待操作；
        #         0：立即返回请求结果；
        #        其他：等待超时时间（单位为秒）
        timex = 5

        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timex)

        # 写数据
        result = ser.write(String.encode("gbk"))
        # result = ser.write(String.decode("hex"))
        print("写总字节数：", result)
        ser.close() # 关闭串口
    except Exception as e:
            print("error!", e)

# usbtransmit("ssss","COM1")
# usbtransmit(chr(0x3c),"COM1")
# usbtransmit(chr(0x4d),"COM1")
# usbtransmit(chr(0x0d),"COM1")
# usbtransmit(chr(0x0a),"COM1")
# usbtransmit(chr(0x3c),"COM1")
# usbtransmit(chr(0x4d),"COM1")

def usbrecieve(recform,len,port):
    """
    通信接受函数
    :return:
    """
    try:
        # 端口：CNU； Linux上的/dev /ttyUSB0等； windows上的COM3等
        portx = "COM2"

        # 波特率，标准值有：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        bps = 115200

        # 超时设置，None：永远等待操作；
        #         0：立即返回请求结果；
        #        其他：等待超时时间（单位为秒）
        # timex = None
        timex = 5
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timex)
        print("串口详情参数：", ser)

        # 十六进制的读取
        s = []
        if recform=="hex":
            for i in range(len+2):
                s.append(ser.read().hex())
            # s1=ser.read().hex()
            # s2=ser.read().hex()
            # print(type(s1))
            # print(ser.read().hex())  # 读一个字节
            # print(ser.read().hex())  # 读一个字节
            # print(s1)
            # print(s2)
            # print("ssss")
            print(s)
            print(int(s[1],16)) # 将16进制字符串转化为10进制整型
        else:
            s1 = ser.read()
            s2 = ser.read()
            s3 = ser.read()
            s4 = ser.read()
            print(s1,s2,s3,s4)
            print(s2)
        print("----------")
        ser.close()  # 关闭串口
    except Exception as e:
        print("error!", e)
    return [10,20]
# while(1):
#     usbrecieve("hex",2,"COM2")
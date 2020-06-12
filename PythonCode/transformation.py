##################### 坐标转换（从小机械臂末端坐标系转换到“织女”的基座标系下  ##################
from numpy import *
from math import *
#######################################################################
#程序基本参数介绍
#theta1 , theta2为2个关节角
#l1,l2为两个关节连杆的长度
#T为转换矩阵（Ts0s1，Ts1s2，Tb0s0）
#P为坐标系下的坐标点(Pb0obj,Ps2obj)物体分别在大机械臂基座标系下坐标，和在小机械臂第二关节坐标系下坐标
#DH参数：
#d为两连杆间的错位距离（平行距离）
#Tb0s0：小机械臂基座标系到大机械臂基坐标系的转换矩阵，即以大机械臂基坐标系为参考
#Ts0s1：小机械臂第一关节坐标系到小机械臂基坐标系的转换矩阵，即以小机械臂基坐标系为参考
#Ts1s2：小机械臂第二关节坐标系到小机械臂第一关节坐标系的转换矩阵，即以小机械臂第一关节坐标系为参考
#xsmallorg，ysmallorg，zsmallorg为小机械臂基座标的原点在大机械臂基座标下的坐标数据
#
#
#详细的理论推理说明，详见机械臂跟随系统.docx文件
#########################################################################################
def transformPic2Cam(Ppicobj):
    """
    将图片坐标系（YY图像目标检测得到的图像坐标  转换为  相机坐标）
    其中，核心是坐标转换矩阵（通过相机标定的到的参数）    MQQ的任务
    Tpic2cam = [ 1  2  3  1
                 5  6  7  8
                 9  9  9  9
                 0  0  0  1 ]
    加上畸变系数，会更加复杂。
    :param Ppicobj:图像坐标（YY任务）
    :return:Pcamobj：相机坐标
    """
    Tpic2cam = mat([[1,2,3,4],
                    [1,2,3,4],
                    [2,3,4,5],
                    [0,0,0,1]
    ])
    Pcamobj = Tpic2cam*Ppicobj
    return Pcamobj

def transformCam2SRend(Pcamobj):
    """

    Tcam2srend = [ 1  2  3  1
                   5  6  7  8
                   9  9  9  9
                   0  0  0  1 ]
    :param Pcamobj: 物体在相机坐标系下的坐标
    :return: Psrendobj:物体在机械臂末端坐标系下的坐标
    """
    Tcam2srend = mat([[1,0,0,0],
                      [0,1,0,0],
                      [0,0,1,0],
                      [0,0,0,1]]
                     )
    Psrendobj = Tcam2srend*Pcamobj
    return Psrendobj

#################新的求解转换函数的程序（利用DH参数）
def transformSRend2SRbase(Psrendobj, theta):
    """
    小机械臂末端坐标系到小机械臂基座标系的坐标转换函数
    DH参数(Craig)：alphai-1    Ai-1    di        thetai
            1        0         0    43.7+76.6   theta1
            2       -90       51.79    0        theta2
            3        0         80    5.86       None
    :param Psrendobj: 物体在小机械臂末端坐标系下的坐标
    :param theta: 2组关节角大小
    :return: Ps0obj：物体在小机械臂基坐标系下的坐标
    """
    #固参
    L2 = 80
    alpha0 = 0
    a0 = 0
    d1 = 43.7+76.6
    alpha1 = -90
    a1 = 51.79
    d2 = 0
    # 变参
    theta1 = theta[0]
    theta2 = theta[1]
    #转换矩阵
    Tsrend2sr2 = mat([[1, 0, 0, L2],
                      [0, 1, 0, 0],
                      [0, 0, 1, 5.86],
                      [0, 0, 0, 1]]
                     )
    Tsr22sr1 = mat([[cos(theta2), -sin(theta2), 0, a1],
                    [sin(theta2) * cos(alpha1), cos(theta2) * cos(alpha1), -sin(alpha1), -sin(alpha1) * d2],
                    [sin(theta2) * sin(alpha1), cos(theta2) * sin(alpha1), cos(alpha1), cos(alpha1) * d2],
                    [0, 0, 0, 1]]
                   )
    Tsr12sr0 = mat([[cos(theta1), -sin(theta1), 0, a0],
                    [sin(theta1) * cos(alpha0), cos(theta1) * cos(alpha0), -sin(alpha0), -sin(alpha0) * d1],
                    [sin(theta1) * sin(alpha0), cos(theta1) * sin(alpha0), cos(alpha0), cos(alpha0) * d1],
                    [0, 0, 0, 1]]
                   )
    #利用转换矩阵求解坐标
    Ps0obj = Tsr12sr0 * Tsr22sr1 * Tsrend2sr2 * Psrendobj
    return Ps0obj

######  小机械臂基坐标系转换到大机械臂“织女”基座标系的坐标转换函数
def transformSRbase2BRbase(Ps0obj):
    """
    从小机械臂基坐标系转换到大机械臂“织女”基座标系的坐标转换函数
    函数内部固定参数：（小机械臂基座标系的原点在大机械臂基座标系下的坐标，取决于两机械臂的相对空间位置）
    xsmall，ysmall，zsmall：小机械臂基座坐标系原点在大机械臂基座坐标系下的坐标
    Tsrbase2brbase = mat([[1,2,3,1],
                        [2,3,4,1],
                        [2,5,6,1],
                        [0,0,0,1]]
                        )
    :param Ps0obj: 物体在小机械臂基坐标系下的坐标
    :return:Pb0obj：物体在大机械臂“织女”基坐标系下的坐标
    """
    xsmallorg = 1
    ysmallorg = 1
    zsmallorg = 1
    Ts02b0 = mat([[1, 0, 0, xsmallorg],
                 [0, 1, 0, ysmallorg],
                 [0, 0, 1, zsmallorg],
                 [0, 0, 0, 1]])
    Pb0obj = Ts02b0*Ps0obj
    return Pb0obj
#########################################################################
# def transformSRendtoBRbase(Ps2obj,theta):
#     """
#     从小机械臂末端坐标系到大机械臂“织女”基座标系的坐标转换函数
#     固定内部参数：（取决于小机械臂的机械结构）
#     d：
#     l1：
#     l2：
#     :param Ps2obj: 物体在小机械臂末端坐标系下的坐标
#     :param theta: 当前小机械臂的各个关节角
#     :return: Pb0obj:物体在大机械臂“织女”基坐标系下的坐标
#     """
#     d = 1
#     l1 = 1
#     l2 = 2
#     # x = 0
#     # y = 0
#     # z = 1
#     theta1 = theta[0]
#     theta2 = theta[1]
#     #Ps2obj = mat([x,y,z,1]).T
#     xsmallorg = 1
#     ysmallorg = 1
#     zsmallorg = 1
#     Tb0s0 = mat([[1,0,0,xsmallorg],
#             [0,1,0,ysmallorg],
#             [0,0,1,zsmallorg],
#             [0,0,0,1]])
#
#     Ts0s1 = mat([[cos(theta1),-sin(theta1),0,0],
#            [sin(theta1),cos(theta1),0,0],
#            [0,             0,       1,0],
#            [0,             0,       0,1]])
#
#     Ts1s2 = mat([[sin(theta2-pi/2),0,sin(pi-theta2),-l2*cos(theta2-pi/2)],
#            [0,1,0,d],
#            [cos(theta2-pi/2),0,cos(pi-theta2),l1+l2*sin(theta2-pi/2)],
#            [0,             0,       0,1]])
#
#     Pb0obj = Tb0s0 * Ts0s1 * Ts1s2 * Ps2obj
#     # print("output the conclusion:")
#     # print(Pb0obj)
#     # print("output the conclusion1:")
#     # print(Pb0obj[0,0])
#     return Pb0obj
#
# #s = transformation()
# #print(s)
# #########################################################################
# #写一个ip/tcp通讯程序（发送程序），向织女实时发送物体在织女基础坐标系下的位置数据，即Pb0obj
# #当得知坐标后立即发送给大机械臂（织女）的控制器，控制其移动到物体的位置处
# # from socket import *
# # def ipcomunication():
# #     server = socket()
# #     server.bind(('127.0.0.1',8180))
# #     server.listen()
# #     conn,client_addr = server.accept()
# #     Pb0obj = transformation()
# #     x = Pb0obj[0,0]
# #     y = Pb0obj[1,0]
# #     z = Pb0obj[2,0]
# #     p = 50
# #     w = 60
# #     r = 90
# #     xstr = "x:" + str(x)
# #     ystr = "y:" + str(y)
# #     zstr = "z:" + str(z)
# #     wstr = "w:" + str(w)
# #     pstr = "y:" + str(p)
# #     rstr = "z:" + str(r)
# #     str1 = xstr + "," + ystr+","+zstr+","+wstr+","+pstr+","+rstr
# #     data = str1.encode()
# #     conn.send(data)
#

#
#
# def transformSRend2SRbase(Psrendobj,theta):
#     """
#     从小机械臂末端坐标系转换到小机械臂基座标系的坐标转换函数
#     内部固定参数：
#     d：
#     l1：
#     l2：
#     Tsrend2srbase = mat([[1,2,3,1],
#                         [2,3,4,1],
#                         [2,5,6,1],
#                         [0,0,0,1]]
#                         )
#     :param Psrendobj: 物体在小机械臂末端坐标系下的坐标
#     :param theta: 小机械臂的各个关节角，此处为二自由度（theta1，theta2）
#     :return: Ps0obj：物体在小机械臂基坐标系下的坐标
#     """
#     d = 1
#     L1 = 1
#     L2 = 2
#     theta1 = theta[0]
#     theta2 = theta[1]
#     Ts0s1 = mat([[cos(theta1), -sin(theta1), 0, 0],
#                  [sin(theta1), cos(theta1), 0, 0],
#                  [0, 0, 1, 0],
#                  [0, 0, 0, 1]])
#
#     Ts1s2 = mat([[sin(theta2 - pi / 2), 0, sin(pi - theta2), -L2 * cos(theta2 - pi / 2)],
#                  [0, 1, 0, d],
#                  [cos(theta2 - pi / 2), 0, cos(pi - theta2), L1 + L2 * sin(theta2 - pi / 2)],
#                  [0, 0, 0, 1]])
#     Ps0obj = Ts0s1*Ts1s2*Psrendobj
#     return Ps0obj



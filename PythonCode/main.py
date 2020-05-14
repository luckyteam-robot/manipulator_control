######## 统筹所有代码，实现目标功能 ########
from transformation import *
from inverse import *
from tcptransmit import *
s = inverse()
# 根据项目流程，链接各模块函数代码

#### 1、目标检测得到物体的位置坐标

#### 2、让小机械臂转动指向物体位置

Ps2obj = mat([0,0,1,1]).T
theta = [0,0]
#### 利用坐标转换矩阵函数将 在小机械臂末端坐标系下的目标物体位姿数据 转换到 “织女”的基座标系下
Pb0obj = transformSRendtoBRbase(Ps2obj,theta)
#### tcp通信，将“织女”坐标系下的目标物体坐标发送给“织女”控制器（服务器地址：192.168.1.100）
tcptransmit(Pb0obj)
#### “织女”控制器接受PC发来的数据进行运动控制
# BRcontrol program
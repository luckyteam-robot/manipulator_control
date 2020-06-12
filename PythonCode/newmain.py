######## 统筹所有代码，实现目标功能 ########
from transformation import *
from inverse import *
from communication import *
from recognize import *
from CameraCapture import *
# 根据项目流程，链接各模块函数代码
#### 1、控制相机拍照
CameraCapture()
#### 2、目标检测得到大机械臂末端的位置坐标
print("正在检测大机械臂末端控制器的位置！")
Ppicobj = recognize("大机械臂末端")          #yy 图像坐标；mqq相机标定得到矩阵，可以将图像坐标转换到相机坐标系下
Pcamobj = transformPic2Cam(Ppicobj)
print("“织女”末端控制器在相机坐标系下的坐标：")
print(Pcamobj)
#### 3、将相机坐标系下的坐标转化到小机械臂末端坐标系下
Psrendobj = transformCam2SRend(Pcamobj)
print("“织女”末端控制器在小机械臂末端坐标系下的坐标：")
print(Psrendobj)
#### 4、获取当前小机械臂的关节角数据（坐标转换矩阵需要用到关节角数据）
usbtransmit("请求关节角数据！","COM1")
theta = usbrecieve("hex",2,"COM2")
print("当前小机械臂的关节角数据：")
print(theta)
#### 5、将小机械臂末端坐标系下的坐标转化到小机械臂基坐标系下
Ps0obj = transformSRend2SRbase(Psrendobj,theta)
print("“织女”末端控制器在小机械臂基座标系下的坐标：")
print(Ps0obj)
#### 6、利用物体在小机械臂基座标系下的坐标，计算出小机械臂指向大机械臂末端时的，小机械臂所呈现的姿态（即求在小机械臂基座标系下的物体的空间角）
print("利用小机械指向“织女”末端执行器时，小机械臂所需呈现的姿态信息（即空间角）：")
thetaspace = NewSpaceAngle(Ps0obj)
print(thetaspace)
#### 7、将小机械臂的2个关节角位置信息通过usb串行通讯传输给STM32，STM32板子即可转动到该指定位置。
print("正在发送关节角信息给STM32，控制小机械臂转向指定位置（即指向“织女”末端执行器）！！！")
usbtransmit(thetaspace,"COM2")
#### 8、小机械臂（即STM32)接收到数据，控制舵机转动至相应角度。
####    SRcontrol program  ￥￥￥￥￥￥
#### 9、控制相机拍照
CameraCapture()
print("控制相机拍照中！！！")
#######################################################################################
#### 10、目标检测算法得到物体的位置坐标
print("正在检测目标物体的位置！")
Ppicobj,kind = recognize("物体")
print("需识别的物体在图像坐标系下的坐标：")
print(Ppicobj)
Pcamobj = transformPic2Cam(Ppicobj)
print("需识别的物体在相机坐标系下的坐标：")
print(Pcamobj)
#### 11、将相机坐标系下的坐标转化到小机械臂末端坐标系下
Ps2obj = transformCam2SRend(Pcamobj)
print("目标物体在小机械臂末端坐标系下的坐标：")
print(Ps2obj)
#### 12、获取当前小机械臂的关节角数据（坐标转换矩阵需要用到关节角数据）
usbtransmit("请求关节角数据！","COM2")
theta = usbrecieve("hex",2,"COM2")
print("当前小机械臂的关节角数据：")
print(theta)
#### 13、利用坐标转换矩阵函数将 在小机械臂末端坐标系下的目标物体位姿数据 转换到 “织女”的基座标系下
Ps0obj = transformSRend2SRbase(Ps2obj,theta)
print("“目标物体在大机械臂基座标系下的坐标：")
print(Ps0obj)
#### 14、利用坐标转换函数 将小机械臂基座坐标系转化到大机械臂基座坐标系
Pb0obj = transformSRbase2BRbase(Ps0obj)
print("“目标物体在大机械臂基座标系下的坐标：")
print(Pb0obj)
#### 15、tcp通信，将“织女”坐标系下的目标物体坐标发送给“织女”控制器（服务器地址：192.168.1.100）
print("将目标物体的位姿信息发送给“织女”控制器")
tcptransmit(Pb0obj)
print("大机械臂运动抓取中！！！")
#### 16、“织女”控制器接受PC发来的数据进行运动控制(在机械臂控制器中使用）
####     BRcontrol program ￥￥￥￥￥￥
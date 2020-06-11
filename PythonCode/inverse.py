#################### 小机械臂运动学反解 ###########################
#input:在小机械臂基座标系下的空间坐标点位数据（x,y,z)或者位姿数据（x,y,z,alpha,belta,omiga)
#output:小机械臂的关节角坐标（theta1,theta2),因为小机械臂暂时为二自由度
#其中的几何图参考，机械臂跟随系统.docx文件中的二自由度机械臂结构图

from numpy import *
import math

####新的计算空间角函数
def NewSpaceAngle(coordinate):
    """
    对于新的二自由度机械臂结构，需要新的几何解法。
    二自由度，具有很大的空间不可达性。
    d：第一杆件和第二杆件的距离（因为两条轴心线呈异面状态）
    L2：第二杆件的长度(事实上，此处用不到）
    Zh：第二关节处（第一连杆和第二连杆交点），距离基座平面的垂直距离
    Xw,Yw,Zw：目标点的世界坐标
    Oh：第二关节处，距离基座轴心线（也可说是第一关节的z轴）的垂直距离
    theta2 = 90 + arctan( (Zh-Zw) / (sqrt(Xw^2+Yw^2)-Oh)
    :param coordinate:
    :return:
    """
    #固定参数(单位均是mm）
    Zh = 70.6 + 6 + 43.7
    Oh = 51.79
    L2 = 80
    d = 5.86
    #可变参数（变量）
    Xw = coordinate[0]
    Yw = coordinate[1]
    Zw = coordinate[2]

    #求解关节角
    #Xw = X' - dsin(theta1)
    #Yw = Y' + dcos(theta1)
    #tan(theta1) = Y' / X'
    #Yw*cos(theta1)-Xw*sin(theta1) = d
    #sqrt(Yw^2+Xw^2) * cos(theta1+phi) = d
    #phi = arctan(Xw/Yw)
    #theta1+phi = arccos( d/sqrt(Yw^2+Xw^2) )
    phi = arctan(Xw/Yw)
    theta1 = arccos(d/sqrt(pow(Yw,2)+pow(Xw,2))) - phi
    X1 = Xw + d*sin(theta1)
    h1 = X1/cos(theta1)
    h2 = h1 - Oh
    theta2 = 90 + arctan((Zh-Zw)/h2)
    return [theta1,theta2]

# def inverse():
#     d = 2
#     L1 = 10
#     L2 = 10
#
#     # 直接利用几何法求解，且解是唯一的，非常简单
#     coordinate = mat([1 , 2 , 3])
#     coordinatex = coordinate[0,0]
#     coordinatey = coordinate[0,1]
#     coordinatez = coordinate[0,2]
# #x = L2cos(theta2-90)*cos(theta1)-d*sin(theta1)
# #y = L2cos(theta2-90)*sin(theta1)+d*cos(theta1)
# #z = L1 + L2*sin(theta2-90)
#
#     theta2 = math.asin((coordinatez - L1)/L2) + 90
#     m = L2*cos(theta2-90)
#     phi = math.atan(d/m)
#     theta1 = math.acos(coordinatex/math.sqrt(math.pow(m,2)+math.pow(d,2))) - phi
#     print(theta1)
#     print(theta2)
#     return [theta1,theta2]
#
#
# ####反解计算空间角的
# def SpaceAngle(coordinate):
#     """
#     计算空间角
#     当需要指向目标位置（此时小机械臂末端根本无法到达该目标点）时，就需计算相对的空间姿态角。
#     :param coordinate: 目标物体的三维坐标
#     :return: theta：相对空间角
#     """
#     L1 = 10
#     d = 2
#     x = coordinate[0]
#     y = coordinate[1]
#     z = coordinate[2]
#     z1 = z - L1
#     #x1 = x + dsin(theta1)
#     #y1 = y - dcos(theta1)
#     #tan(theta1) = y1/x1
#     #tan(theta2) = z1/sqrt(x1^2+y1^2)
#     phi = math.atan(y/x)
#     theta1 = math.asin(-d/sqrt(math.pow(x,2) + math.pow(y,2))) + phi
#     theta2 = math.atan(z1/sqrt(math.pow(x+d*sin(theta1),2) + math.pow(y-d*cos(theta1),2)))
#     return [theta1,theta2]


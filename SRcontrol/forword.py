#################### 小机械臂运动学正解 ###########################
#input：关节坐标（theta1，theta2）
#output：小机械臂末端在小机械臂基座标系下的坐标
import numpy
import math
#小机械臂的基本参数
L1 = 10
L2 = 10
d = 2
#输入参数（theta1，theta2）
theta1 = 0
theta2 = 90
##直接利用几何法，非常简单
x = L2*math.cos(theta2-90)*math.cos(theta1)-d*math.sin(theta1)
y = L2*math.cos(theta2-90)*math.sin(theta1)+d*math.cos(theta1)
z = L1 + L2*math.sin(theta2-90)
print(x)
print(y)
print(z)
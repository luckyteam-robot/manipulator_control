from numpy import *

def recognize(type):
    """
    目标检测函数，输出目标物体的图像坐标
    :param type: 需要检测的物体类型
    :return: 需检测物体的位置信息
    """
    import detect   #运行detect文件
    # print(detect.a )      #detect.a访问detect.py文件中的变量a
    ordination = mat([0, 0, 1, 1]).T
    Str = " "
    if(type=="机械臂末端"):
        return ordination
    if(type=="物体"):
        return ordination,Str
    return mat([0, 0, 1, 1]).T
recognize("wuti")
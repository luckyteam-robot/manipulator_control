from numpy import *
# import detect
# import os
def recognize(type):
    # os.system('python detect.py')
    # os.system('python main.py')
    # os.popen('python /home/learngod/GitHub/manipulator_control/PythonCode/MaskRCNN-Recognize/detect.py')
    import detect
    ordination = mat([0, 0, 1, 1]).T
    Str = " "
    if(type=="机械臂末端"):
        return ordination
    if(type=="物体"):
        return ordination,Str

    return mat([0, 0, 1, 1]).T

recognize("sss")
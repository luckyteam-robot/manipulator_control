from numpy import *
def recognize(type):
    ordination = mat([0, 0, 1, 1]).T
    Str = " "
    if(type=="机械臂末端"):
        return ordination
    if(type=="物体"):
        return ordination,Str

    return mat([0, 0, 1, 1]).T
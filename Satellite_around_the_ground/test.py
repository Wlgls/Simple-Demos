
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2019/11/28 09:27:44
@Author  :   Wlgls 
@Version :   1.0
@Contact :   smithguazi@gmail.com
'''


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as amt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D


def get_config(t, r=6400, v=10):
    """求解二阶微分方程，二阶微分方程见图片，为了便于求解，将二阶微分方程转换为一阶微分方程
    即： 定义
        y1 = r 极坐标
        y2 = /theta 初始角度
        y3： 初始径向线速度
        y4: 初始角速度
        其一阶微分方程为：
        y1'=y3
        y2'=y4
        y3'=-K/(y1*y1) + y1*y4*y4
        y4'=-2*y3*y4/y1
    
    Args:
        t (int): 离散的时间变量，t为结束时间
        r (int): 近地点的距离
        v (int): 发射的速度
    
    Returns:
        [list]: 返回[y1, y2, y3, y4]
    """   
    
    ti = np.arange(0, t, 0.5)   # 以0.5切片，求解，离散量
    def run(w, t, k):
        y1, y2, y3, y4 = w
        return y3, y4, -k/(y1*y1)+y1*y4*y4, -2*y3*y4/y1

    k = 401408  # 地球重力系数

    w0 = (r, np.pi, 0, v/r) # 使用np.pi可以使卫星从左侧开始转圈圈
    
    result = odeint(run, w0, ti, args=(k,))
    return result


def update(t, r, v, angel):
    """
    用于FunAnimation的函数，定义了每一帧时的状态
    
    Args:
        t (int): 为了形成轨迹，时间t是递增的，事实上，这也许不合理，
        r (int): 近地点的距离
        v (int): 发射的速度
        angel(int): 发射时的角度
    """    

    global ln, ln2
    
    result = get_config(t, r, v)  # 求解  r和/theta
    
    # 速度太低，会卫星
    flag = result[1:,0] > 6400
    if not np.all(flag==True):
        print("没有飞起来。。。")
        exit()


    # 这个是卫星的图像
    rho, the = result[-1, 0:2] if len(result) !=0 else (-r, 0)  
    xt = rho * np.cos(the)
    yt = rho * np.sin(the) * np.cos(angel)
    zt = rho * np.sin(the) * np.sin(angel)
    ln2.set_data([xt], [yt])
    ln2.set_3d_properties([zt])
    
    #  这是轨迹的图像
    x = result[:, 0] * np.cos(result[:, 1])
    y = result[:, 0] * np.sin(result[:, 1]) * np.cos(angel)
    z = result[:, 0] * np.sin(result[:, 1]) * np.sin(angel) # 我只能实现简单的旋转，再复杂一些，我就不会了，但很明显，这不是现实中应有的结果
        
    ln.set_data(x,y)
    ln.set_3d_properties(z)
    return ln2,ln


def draw_sphere(ax, r=6400):
    """
    画一个球体
    
    Args:
        ax : 用于作画的坐标戏
        r : 球体的半径
    """
    alpha, psi = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    ex =r * np.sin(psi) * np.cos(alpha)
    ey =r * np.sin(psi) * np.sin(alpha)
    ez =r * np.cos(psi)
    ax.plot_wireframe(ex, ey, ez, color='r')

def set_config():
    """
    输入数据
    Returns:
        [Tuple]: 返回速度， 近地点高度， 角度
        其中，角度是与Y轴负方向的夹角
    """         
    r = input('输入近地点高度(默认为6400Km)')
    v = input('输入初始速度(默认为10Km/s)')
    angel = input('输入初始角度(默认为0度)')
    if not((r=="" or r.isalnum()) \
        and (v=="" or v.isalnum()) \
        and (angel=="" or angel.isalnum())):
        print("请只输入数字")
        set_config()

    r = int(r) if r != "" else 6400
    v = int(v) if v != "" else 10
    angel = int(angel)/180*np.pi if angel != "" else 0
    return (r, v, angel)

if __name__ == '__main__':

    # r, v, angel = set_config()    # 如果要手动输入将下面的注释掉，然后将这一行取消注释
    r = 7000
    v = 7.9
    angel = 0

    f = plt.figure(figsize=(10,10))
    ax = f.add_subplot(111, projection='3d')    

    ax.set_xlim([-50000, 50000])    # 由于稍微改一点就会超出坐标系，如果想要得到更好的数据，请修改坐标系
    ax.set_ylim([-50000, 50000])
    ax.set_zlim([-50000, 50000])
    # ax.set_zlim([-0.2, 0.2])    # x, y, z坐标系
    # earth
    
    draw_sphere(ax, 6400)


    ln, = ax.plot([], [], [], color='purple')   # 轨迹

    ln2, =ax.plot([], [], [], marker='o', color='black',markersize=8)   # 卫星


    ani = amt.FuncAnimation(f, update,frames=range(0, 100000, 100),fargs=(r, v, angel),interval=2)
    plt.show()

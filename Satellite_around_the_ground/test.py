
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


def get_config(t):
    """求解二阶微分方程，为了便于求解，将二阶微分方程转换为一阶微分方程
    即： 定义
        y1 = r  地球半径
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
    
    Returns:
        [list]: 返回[y1, y2, y3, y4]
    """   
    global r
    ti = np.arange(0, t, 0.5)   # 以0.5切片，求解，离散量
    def run(w, t, k):
        y1, y2, y3, y4 = w
        return y3, y4, -k/(y1*y1) + y1*y4*y4, -2*y3*y4/y1

    # v, w0 = set_config()

    v = 10
    w0 = (r, 0, 0, v/r) # 暂时先这么设置，后面再改
    
    result = odeint(run, w0, ti, args=(k,))
    return result
    
    


def update(t):
    global ln
    result = get_config(t)
    # print(result)
    rho, the = result[-1, 0:2] if len(result) !=0 else (r, 0)
    xt = rho * np.cos(the)
    yt = rho * np.sin(the)
    ln2.set_data([xt], [yt])
    ln2.set_3d_properties([0])

    x = result[:, 0] * np.cos(result[:, 1])
    y = result[:, 0] * np.sin(result[:, 1])
    ln.set_data((x, y))
    ln.set_3d_properties(0)
    return ln, ln2

def draw_circle(ax, r):
    """
    画一个球体
    
    Args:
        ax ([type]): [description]
        r ([type]): [description]
    """
    alpha, psi = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    ex =0 + r * np.sin(psi) * np.cos(alpha)
    ey =0 + r * np.sin(psi) * np.sin(alpha)
    ez =0 + r * np.cos(psi)
    ax.plot_wireframe(ex, ey, ez, color='blue')




k = 401408  # 地球重力系数
r = 6400    # 地球半径

f = plt.figure(figsize=(6,6))
ax = f.add_subplot(111, projection='3d')
# ax.axis('equal')
ax.set_xlim([-20000, 20000])
ax.set_ylim([-20000, 20000])
ax.set_zlim([-20000, 20000])
# earth
 # alpha, psi = np.arange(0, np.pi*2, 0.01)    # 球体，竖直平面180,水平360
draw_circle(ax, r)
# ax.fill(ex, ey, ez, 'r')

ln, = ax.plot([], [], [], color='purple')
ln2, =ax.plot([], [], [], marker='o', color='red',markersize=8)
t = np.arange(0, 100000, 0.5)    # 时间t

# plt.show()

ani = amt.FuncAnimation(f, update,frames=range(0, 100000, 100),interval=20)
plt.show()

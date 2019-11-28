
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def draw_circle(ax, r):
    t = np.arange(0, np.pi*2, np.pi/360)
    x = r * np.cos(t)
    y = r * np.sin(t)
    z = np.zeros(len(t))
    ax.plot(x, y, z)

def drwa_my(ax2):
    global ln2
    t = 20000
    ti = np.arange(0, t, 0.5)   # 以0.5切片，求解，离散量
    def run(w, t, k):
        y1, y2, y3, y4 = w
        return y3, y4, -k/(y1*y1)+y1*y4*y4, -2*y3*y4/y1

    k = 401408  # 地球重力系数
    v = 10
    r = 6400
    w0 = (r, np.pi, 0, v/r) # 暂时先这么设置，后面再改
    
    result = odeint(run, w0, ti, args=(k,))

    x = result[:, 0] * np.cos(result[:, 1])
    y = result[:, 0] * np.sin(result[:, 1])
    z = np.zeros(len(result), dtype=np.uint8)
    ln2, = ax2.plot(x, y, z)
    return ln2

if __name__ == '__main__':
    fig = plt.figure(figsize=(9,6))
    #添加参数projection
    ax1 = fig.add_subplot(121,projection='3d')
    draw_circle(ax1, 10)
    ax2 = fig.add_subplot(122,projection='3d')
    drwa_my(ax2)
    # drwa_my()
    plt.show()
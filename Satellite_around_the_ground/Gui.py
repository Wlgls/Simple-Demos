# -*- encoding: utf-8 -*-
'''
@File    :   GUI.py
@Time    :   2019/11/29 11:55:31
@Author  :   Wlgls 
@Version :   1.0
@Contact :   smithguazi@gmail.com
'''

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import Satellite as Salt
from tkinter import ttk
from tkinter import messagebox

TrackOptions = ['一般卫星','极地卫星', '同步卫星']

DEFAULT_R = 6400
DEFAULT_V = 10
DEFAULT_ANGEL = 0   # 默认值

class GUIframe(tk.Frame):
    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.grid() 
        self.createWidgets()    # 初始化，创建事件
    
    def createWidgets(self):
        
        self.TrackLabel = tk.Label(self, text='卫星轨道:')  
        self.TrackTypeVar = tk.StringVar(self)
        self.TrackTypeVar.set(TrackOptions[0])
        self.TrackOptions = tk.OptionMenu(*((self, self.TrackTypeVar) + tuple(x for x in TrackOptions)))
        self.TrackOptions.configure(width=14)   
        self.TrackLabel.grid(row=1, column=0, sticky=tk.W)
        self.TrackOptions.grid(row=1, column=1, sticky=tk.W + tk.E)
        self.TrackTypeVar.trace("w", self.track)    # Track的选择，提供了三种发射方式

        tk.Label(self, text="近地点高度：").grid(row=0, column=4, sticky=tk.W)
        self.r = tk.Entry(self)
        self.r.insert(0, DEFAULT_R)
        self.r.grid(row=0, column=5, sticky=tk.W+tk.E)  # 近地点高度

        tk.Label(self, text="初始速度：").grid(row=1,column=4, sticky=tk.W)
        self.v = tk.Entry(self)
        self.v.insert(0, DEFAULT_V)
        self.v.grid(row=1, column=5, sticky=tk.W+tk.E)  # 初始速度

        tk.Label(self, text="初始角度").grid(row=2,column=4, sticky=tk.W)
        self.angel = tk.Entry(self)
        self.angel.insert(0, DEFAULT_ANGEL)
        self.angel.grid(row=2, column=5, sticky=tk.W+tk.E)  # 初始角度
        
        # 由于为了好看，我设定了8个级别的坐标系
        self.ScaleLabel = tk.Label(self, text='坐标系尺度:')
        self.ScaleTypeVar = tk.IntVar(self)
        self.ScaleTypeVar.set(5)
        self.ScaleOptions = tk.OptionMenu(*((self, self.ScaleTypeVar) + tuple(x+1 for x in range(8))))
        self.ScaleOptions.configure(width=14)       # 设计坐标系尺度
        self.ScaleLabel.grid(row=4, column=4, sticky=tk.W)
        self.ScaleOptions.grid(row=4, column=5, sticky=tk.W + tk.E)
        self.ScaleTypeVar.trace("w", self.track)    

        tk.Button(self, text="发射", width=10, command=self.Start).grid(row=4, column=0,sticky=tk.W + tk.E) # 事件，点击发射键，开始模拟

        tk.Button(self, text="退出", width=10, command=self.master.quit).grid(row=4, column=1,sticky=tk.W + tk.E)   # 推出键

    def get_Track(self):
        # 得到Track数据
        index = TrackOptions.index(self.TrackTypeVar.get())
        return index

    def track(self, *args):
        # 监控Track， 给使用着提供警告
        track = self.get_Track()
        if track == 1:
            messagebox.showwarning('Warning', '选择极地卫星，意味着你输入的角度不可用', parent=self)
        elif track == 2:
            messagebox.showwarning('Warning', '同步卫星有固定参数，你所设定的参数无用!', parent=self)

    def get_R(self):
        # 得到R
        R = DEFAULT_R
        try:
            R = float(self.r.get())
        except:
            uiutils.error('You entered an invalid k1! Please try again.')
        return R

    def get_V(self):
        # 得到V
        V = DEFAULT_V
        try:
            V = float(self.v.get())
        except:
            uiutils.error('You entered an invalid k1! Please try again.')
        return V

    def get_Angel(self):
        # 得到角度
        Angel = DEFAULT_ANGEL
        try:
            Angle = float(self.angel.get())
        except:
            uiutils.error('You entered an invalid k1! Please try again.')
        return Angel

    def get_Scale(self):
        # 得到坐标系尺度
        Scale = self.ScaleTypeVar.get()
        return Scale * 10000

    def Start(self):
        # 开始模拟
        Track = self.get_Track()
        V = self.get_V()
        R = self.get_R()
        Angel = self.get_Angel() if Track!=1 else np.pi/2
        Scale = self.get_Scale()    #  得到需要的数据

        if R < 6400:        # 判断高度，如果R小于6400, 则弹出提示框
            message = "你的高度是{}, 也许是你想在地下发射卫星".format(R)
            messagebox.showerror('Error', message, parent=self)
            return  
            
        f = plt.figure(figsize=(10, 10))    # 画图
        ax = f.add_subplot(111, projection='3d') 
        self.show_Track(f, ax, V, R, Angel, Scale, Track)   # 调用show_track开始画图

    def show_Track(self,f, ax, V, R, Angel, Scale, Track):
        
        ax.set_xlim([-Scale, Scale])    # 由于稍微改一点就会超出坐标系，如果想要得到更好的显示，请修改坐标系
        ax.set_ylim([-Scale, Scale])
        ax.set_zlim([-Scale, Scale])

        f, ani, flag = Salt.draw_satellite(f, ax, v=V, r=R, angel=Angel, track=Track)   # 调用satellite.py中的函数，开始模拟

        if flag == 0:   # 在运行过程中如果低于6400，则意味着卫星撞地球
            messagebox.showerror('Error', '你的卫星太慢了，以至于撞到了地球，为了保护世界，我必须终止程序', parent=self)
            return

        plt.show()
    
    
if __name__ == '__main__':

    master = GUIframe() # 调用函数，启动GUI
    master.mainloop()   # 必要函数，循环
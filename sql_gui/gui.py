# -*- encoding: utf-8 -*-
'''
@File    :   gui.py
@Time    :   2019/11/30 16:14:05
@Author  :   Wlgls 
@Version :   1.0
@Contact :   smithguazi@gmail.com
'''

import tkinter as tk
from tkinter import messagebox
import sqlfunc as qf
from tkinter import ttk

columnoptions = (('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'))

class ConnectFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        tk.Label(self, text="用户").grid(row=1, column=0, sticky=tk.W)
        self.username = tk.Entry(self)
        self.username.grid(row=1, column=1, sticky=tk.W+tk.E)

        tk.Label(self, text="密码").grid(row=2, column=0, sticky=tk.W)
        self.password = tk.Entry(self)
        self.password.grid(row=2, column=1, sticky=tk.W+tk.E)

        tk.Button(self, text="链接", width=10, command=self.connect).grid(row=3, column=1,sticky=tk.W + tk.E)

    def connect(self):
        username = self.username.get()
        password = self.password.get()

        flag = qf.connect(username, password)   # 调用链接函数，失败返回false
        # flag = True
        if flag:
            self.destroy()
            baseFrame(self.root,self.root)
            # baseFrame()
        else:
            messagebox.showerror(self, "密码或用户名错误")

class baseFrame(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.notebook.add(ShowFrame(self.notebook, root), text="show")
        self.notebook.add(InsertFrame(self.notebook, root), text='insert')
        self.notebook.grid(row=0, sticky=tk.N+tk.S+tk.E+tk.W)
    
class ShowFrame(tk.Frame):
    def __init__(self, notebook, root):
        ttk.Frame.__init__(self, notebook)
        self.numberVar  = tk.IntVar()
        tk.Label(self, text="查询数量").grid(row=0, column=2, sticky=tk.W)
        tk.Radiobutton(self, text='50', variable=self.numberVar, value=50
                        ).grid(row=0, column=5, sticky=tk.W)
        tk.Radiobutton(self, text='1000', variable=self.numberVar, value=1000
                        ).grid(row=0, column=6, sticky=tk.E)
        self.numberVar.set(50)
        tk.Button(self, text='查询', command=self.ShowTopData 
                        ).grid(row=0, column=8, sticky=tk.W)
    
    def ShowTopData(self):
        num = self.numberVar.get()
        data = qf.selecttopdata(num)

        dataTreeview = ttk.Treeview(self,show='headings', column=[column[0] for column in columnoptions])
        dataTreeview.place(rely=0.3, relwidth=0.97)
        for column in columnoptions:
            dataTreeview.column(column[0], width=200, anchor="center")
            dataTreeview.heading(column[0], text=column[1])

        for item in data:
            dataTreeview.insert("","end", value=item)

        dataTreeview.grid(row=4, column=12, sticky=tk.NSEW, ipadx=10)
        
class InsertFrame(tk.Frame):
    def __init__(self, notebook, root):
        ttk.Frame.__init__(self, notebook)
        


if __name__ == '__main__':
    root = tk.Tk()
    # app = ConnectFrame(root)
    app = baseFrame(root, root)
    w, h = root.winfo_screenwidth(), root.winfo_screenheight() - 50
    root.geometry("%dx%d+0+0" % (w, h))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    app.mainloop()
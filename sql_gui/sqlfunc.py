# -*- encoding: utf-8 -*-
'''
@File    :   sqlfunc.py
@Time    :   2019/11/30 16:44:09
@Author  :   Wlgls 
@Version :   1.0
@Contact :   smithguazi@gmail.com
'''

def connect(username, password):
    """链接数据库
    
    Args:
        username ([str]): 用户名
        password ([str]): 密码
    Return:
        flag： 返回标志，成功或者失败
    """    
    return True


def selecttopdata(num):
    """ 查询数据，简单的查询前num个数据

    Args:
        num ([int]): 数量
    """    

    data = [[1, 2, 3, 4], [2, 3, 4, 5]]
    return data
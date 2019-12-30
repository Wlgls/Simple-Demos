# -*- encoding: utf-8 -*-
'''
@File    :   rm_pic_redun.py
@Time    :   2019/12/28 20:21:10
@Author  :   Wlgls 
@Version :   1.0
@Contact :   smithguazi@gmail.com
'''

from pathlib import Path
import re
import os
from urllib.request import quote

def get_files(dir_name):
    """得到指定目录下的所有文件生成器

    Args:
        dir_name (Str): 指定目录
    Return:
        files generator: 文件生成器
    """ 

    p = Path(dir_name)
    if p.exists():
        return p.iterdir()


def find_pics(f, target):
    """
    获取文件中的内容，并寻找文件中的图片的名字
    由于前期就各种乱搞，有的是使用sm.ms的图床，有的又是基于网络路径的，本地看不了。
    后来就使用typora，所以，匹配的可能要麻烦一些
    Args:
        f (PosixPath): 文件名称
        target : 从网络上下载图片后保存的目录位置
    
    Returns:
        pics: 图片名称列表
        index: 文件索引位置
    """    
    pics = []
    index = []

    content = f.read_text()
    contents = content.split('\n')

    pattern = re.compile(r'\!\[(.*)\]\((.*)\)')
    for i in range(len(contents)):
        re_match = pattern.match(contents[i])
        if re_match != None: 
            re_match = re_match.groups()

            pic = re_match[1]# 这个是![]()小括号里的内容

            # 由于最开始就各种尝试，所以就图片链接乱七八糟
            pic_name = re.match(r'^https?:.*/(.*)$',pic)
            if pic_name != None:
                pic_name = 'image-'+re_match[0]
                os.system('wget {} -O {}'.format(pic, target+pic_name))
            else:
                pic_name = re.match(r'.*/(.*)$', pic)
                if pic_name != None:
                    pic_name = pic_name.groups()[0]
                else:
                    pic_name = pic
            index.append(i)
            pics.append(pic_name)
    print(len(pics))
    return pics, index

def repath_pic(pics, target):
    """
    将图片移动到指定文件目录中
    图片放在../posts/文件中，需要生成PosixPath对象
    Args:
        pics (list): 图片列表
        target (Str): 目标目录
    """
    f_pic = Path(target)    #要转移的路径
    if not f_pic.exists():
        # print(f_pic)
        f_pic.mkdir()
    r_pic = f_pic.parent     
    # 取个巧，因为我就是在我现在存放的文件里分类一下，如果要修改还是要添加一个参数的
    
    r_pics = [r_pic.joinpath(item) for item in pics]
    targets = [target + '/' + item for item in pics]
    for pic, t in zip(r_pics, targets):
        if pic.exists():
            pic.replace(t)
        else:
            print('ERROR {}'.format(t))
    
def rewrite_pic_in_file(pics, index, f, target):
    """
    文章中的图片链接更改一下
    
    Args:
        pics (list): 图片名称列表
        index (list): 索引位置
        f (PosixPath): 文件名称
        target : 目标格式![{pic}]../posts/{title}/{pic}
    """ 
    title = f.stem
    # 将中文编码
    # TODO-BEGIN
    title = quote(title)
    # TODO-END
    pattern = re.compile(r'^\!\[.*\]\(.*\)')
    content = f.read_text()
    contents = content.split('\n')
    for i, pic in zip(index, pics):

        contents[i] = re.sub(pattern, target.format(title=title,pic=pic), contents[i])
    # pass
    content = '\n'.join(contents)
    f.write_text(content)

def main():
    dir_name = '/home/smith/Blog/_posts'
    base_name = '/home/smith/Blog/posts'
    tar_format = '![{pic}](../posts/{title}/{pic})'
    files = get_files(dir_name)
    for f in files:
        title = f.stem
        print(title)
        pics, index = find_pics(f, base_name)
        repath_pic(pics, base_name+'/'+title)
        rewrite_pic_in_file(pics, index, f, tar_format)
        input()


if __name__ == '__main__':
    """ f = '/home/smith/Data/test/test.md'
    target = '/home/smith/Data/test/'
    f = Path(f)
    find_pics(f, target) """
    main()
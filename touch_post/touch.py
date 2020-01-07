# -*- encoding: utf-8 -*-
'''
@File    :   generate_file.py
@Time    :   2020/01/07 22:48:15
@Author  :   Wlgls 
@Version :   2.0
@Contact :   smithguazi@gmail.com
'''

import time
from pathlib import Path
import readline

base_dir = '/home/smith/Blog/_posts'    # 文章所在目录
title_format = '%Y-%m-%d-{}.md'     # 文章标题命名格式
title = time.strftime(title_format, time.localtime())    # 将当前时间设置为title

layout = 'post' # layout
params_name = ['layout', 'title', 'categories'] # 文章的头标题
content_header = '''
---
layout: {layout}
title: {title}
categories: {categories}
---

* content 
{:toc}
'''

def get_params():

    params_value = [eval("input('{}:')".format(item)) for item in params_name[1:]]
    params_value.insert(0, layout)
    params = dict(zip(params_name, params_value))

    # 在这里顺便把title也给确定了
    title_format.format(params['title'])
    return params
    
def set_content(params): 
    # 取巧，对于{:toc}在使用format函数时，很不方面，所以直接将后面的给截掉是一种取巧的手段
    content_header[:-10].format(**params)

def touch():

    p = Path(base_dir + title)

    if not p.exists():
        p.touch()

    p.write_text(content_header)


if __name__ == '__main__':
    params = get_params()
    # params = {'layout': 'post', 'title': 'adf', 'categories': 'asddf'}
    set_content(params)
    touch()
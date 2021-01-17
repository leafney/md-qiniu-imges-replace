#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-------------------------------
@File    : qiniu_img_to_gitee.py
@Desc    : 查找markdown文档中的图片链接
@Time    : 2021-01-16 15:34:19
@Author  : leafney
@Version : v1.0
-------------------------------
'''


import os
import re
import time

count = 0

def md_read(md_file):
    file=''
    with open(md_file,'r') as f:
        file=f.read()
    return file

def md_write(md_file,str):
    with open(md_file,'w') as f:
        f.write(str)


def md_img_replace(md_file):
    global count
    result=False
    post=md_read(md_file)
    matches = re.compile(
        '!\\[.*?\\]\\((.*?)\\)|<img.*?src=[\'\"](.*?)[\'\"].*?>').findall(post)
    
    if matches and len(matches)>0:
        # 该md文件中有图片

        # 输出文件名称
        print('文件：[{0}] 中含有图片'.format(md_file))
        new_post=post
        for sub_match in matches: # 正则里包含或，所以这里sub_matth是元组
            # print(sub_match)
            for match in sub_match:
                if match and len(match)>0:
                    # 得到单张图片链接
                    print('找到图片链接：[{0}]'.format(match))
                    count+=1
        
        print('**************** count={0} ******'.format(count))

    return True

def main():
    global count
    path = "./_posts"
    files=os.listdir(path)
    i=0
    for file in files:
        if not os.path.isdir(file) and file[file.rfind('.') + 1:] == 'md':
            # 如果是文件
            # print(file)
            p = path + '/' + file
            if md_img_replace(p):
                # break
                pass
            i+=1
        
        time.sleep(2)

    print(i)
    print('共找到图片 {0} 张'.format(count))


if __name__ == "__main__":
    main()
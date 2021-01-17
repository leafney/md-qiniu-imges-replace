#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-------------------------------
@File    : qiniu_img_to_gitee.py
@Desc    : 将博客中的七牛云图片链接替换为gitee仓库图片链接
@Time    : 2021-01-16 15:34:19
@Author  : leafney
@Version : v1.0
-------------------------------
'''


import os
import re
import time
import requests
from urllib.parse import urlsplit,urlunsplit,urljoin

# 去除https的提醒
requests.packages.urllib3.disable_warnings()

def md_read(md_file):
    file=''
    with open(md_file,'r') as f:
        file=f.read()
    return file

def md_write(md_file,str):
    with open(md_file,'w') as f:
        f.write(str)


def md_img_replace(md_file):
    result=False
    post=md_read(md_file)
    matches = re.compile(
        '!\\[.*?\\]\\((.*?)\\)|<img.*?src=[\'\"](.*?)[\'\"].*?>').findall(post)
    
    matches_count=len(matches)
    if matches and matches_count>0:
        # 该md文件中有图片

        # 输出文件名称
        print('文件：[ {} ] 中含有 {} 张图片'.format(md_file,matches_count))
        new_post=post
        for sub_match in matches: # 正则里包含或，所以这里sub_match是元组
            # print(sub_match)
            for match in sub_match:
                if match and len(match)>0:
                    # 得到单张图片链接
                    print('找到图片链接：[ {} ]'.format(match))

                    # 筛选图片链接，只对特定的图片链接进行处理
                    # https://qiniu.itfanr.cc/blog/20210116213144.png?imageslim
                    # https://qiniu.itfanr.cc/blog/171117/lggD4efImf.png?imageslim

                    if match.startswith('https://qiniu.itfanr.cc'):
                        # 先下载图片，图片下载成功后，替换文章中图片的链接为新链接

                        # 去除图片的后缀 ?imageslim，这个是对图片进行优化的，这里要下载原图片
                        match_down_url = parse_url_link(match)

                        # 保存图片到本地
                        (is_down_ok,file_name) = download_file(match_down_url)
                        if is_down_ok:
                            print('图片 [ {} ] 下载成功，保存到本地 {}'.format(match_down_url,file_name))
                        else:
                            print('图片 [ {} ] 下载失败'.format(match))
                            
                        # 只有下载成功的图片才进行替换操作
                        if is_down_ok:
                            # 记录下替换前的链接
                            old_url=match
                            
                            """
                            # 优化后：这里不用这段了
                            # 替换目录前面的域名及基础目录，注意这里用的是原图片的下载url，不含 ?imageslim 的那种
                            # new_url = match_down_url.replace(
                            #     'https://qiniu.itfanr.cc', 'https://gitee.com/leafney/blogimage/raw/master')
                            """

                            # 对于 https://qiniu.itfanr.cc/blog/171117/AkL6GebFaB.png?imageslim 的图片，处理链接为
                            # https://gitee.com/leafney/blogimage/raw/master/blog/171117AkL6GebFaB.png
                            # 即将 blog 目录后的一级目录合并为文件名，那么 上面保存到本地的文件路径即为处理后的路径，所以可以直接拼接：
                            
                            new_url = urljoin('https://gitee.com/leafney/blogimage/raw/master/',file_name) # 注意 urljoin拼接时，最后要加/，否则就是上一级目录了

                            print('替换后的图片路径为:[ {} ]'.format(new_url))

                            # 替换 post 文件中的 old_url为 new_url，并将新内容写回文件
                            new_post = new_post.replace(old_url, new_url)

                            result = True
                            # sleep
                            time.sleep(1)

                    else:
                        print('图片 [ {} ] 不符合处理规则，跳过不处理'.format(match))

                    print('----------------')

        if result:
            # 将内容重新写回文件
            # print(new_post)
            md_write(md_file,new_post)
            print('ok-修改成功')

        print('****** 即将处理下一个文件 **********')
    return result

def download_file(img_path):
    """
    下载图片资源到本地
    规定图片默认以 blog 开头，所以图片在本地路径为 `blog/171117h0GeCiKJG3.png` ,即会保存到本地 `blog` 目录下
    """
    res = False
    # 获取保存时的文件名
    file_name=parse_image_name(img_path)

    r = requests.get(img_path,stream=True,verify=False)
    if r.status_code == 200:
        content =r.content

        # 创建目录
        dir_name=os.path.dirname(file_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        # 写入二进制文件
        with open(file_name,"wb") as f:
            f.write(content)
        
        res=True
    
    return (res,file_name)


def parse_image_name(url):
    """
    解析拆分url，拼接成图片的新名称
    只处理图片路径 path 部分以 blog 开头的，分两种情况：

    https://qiniu.itfanr.cc/blog/171117/h0GeCiKJG3.png ==> blog/171117h0GeCiKJG3.png  将二级目录合并为一级目录
    https://qiniu.itfanr.cc/blog/20190223160142.png ==> blog/20190223160142.png
    """

    res=""
    urls = urlsplit(url)
    url_path=urls.path
    # print(url_path)
    # 对路径中的path部分通过/分隔，去除为空的项
    ups = [x for x in url_path.split('/') if x.strip()]
    # print(ups)
    if len(ups)>1:
        ups_first=ups[0]
        if ups_first == "blog":
            ups.pop(0)
            res=ups_first+'/'+ ''.join(ups)
    else:
        res=''.join(ups)
        print('发现异常图片路径：{0}'.format(res))
    
    return res


def parse_url_link(url,file_name=''):
    """
    url：图片url链接
    file_name: 指定的图片文件名
    处理图片链接，去除后面携带的参数
    https://gitee.com/leafney/blogimage/raw/master/blog/20190904123229.png?imageslim 
     ==> 
    https://gitee.com/leafney/blogimage/raw/master/blog/20190904123229.png
    """
    urls = urlsplit(url)
    # print(urls)
    new_path=urls.path
    if file_name!='':
        new_path=file_name

    new_url=urlunsplit((urls.scheme,urls.netloc,new_path,'',''))
    # print(new_url)
    return new_url


def main():
    
    path = "./_posts"
    files=os.listdir(path)
    i=0
    for file in files:
        if not os.path.isdir(file) and file[file.rfind('.') + 1:] == 'md':
            # 如果是文件
            # print(file)
            p = path + '/' + file
            if md_img_replace(p):
                break # 只处理一个文件，用来测试
                # pass 
            i+=1
        
        time.sleep(2)

    
    print(i)


def test():

    # u="https://qiniu.itfanr.cc/blog/171117/h0GeCiKJG3.png"
    # u="https://qiniu.itfanr.cc/blog/20190223160142.png"
    # print(parse_image_name(u))
    # print(download_file(u))

    # u2="https://gitee.com/leafney/blogimage/raw/master/blog/20190904123229.png?imageslim"
    # parse_url_link(u2)

    print(urljoin('https://gitee.com/leafney/blogimage/raw/master/','blog/20190223160142.png'))

    pass


if __name__ == "__main__":
    # main()

    test()



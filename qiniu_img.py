#coding:utf-8

import re
import os
import time


def md_read(md_file):
    file=''
    with open(md_file,'r') as f:
        file=f.read()
    return file

def md_write(md_file,str):
    with open(md_file,'w') as f:
        f.write(str)

def md_img_replace(md_file):
    """
    替换md文件中的图片链接
    """
    result=False
    post=md_read(md_file)
    matches = re.compile(
        '!\\[.*?\\]\\((.*?)\\)|<img.*?src=[\'\"](.*?)[\'\"].*?>').findall(post)
    
    if matches and len(matches)>0:
        # 该md文件中有图片

        # 输出文件名称
        print('文件：[{0}] 中含有图片'.format(md_file))
        new_post=post
        for sub_match in matches: # 正则里包含或，所以这里sub_match是元组
            # print(sub_match)
            for match in sub_match:
                if match and len(match)>0:
                    # 得到单张图片链接
                    print('找到图片链接：[{0}]'.format(match))
                    # 在这里遍历一遍后，发现我的文章中图片链接的特点主要有三种格式：
                    """
                    https://qiniu.itfanr.cc/blog/20180924112100.png?imageslim  -- 已经符合要求的
                    http://ouej55gp9.bkt.clouddn.com/blog/20180920204113.png   -- 只有旧版链接的
                    http://ouej55gp9.bkt.clouddn.com/blog/180116/B2c2Deah5B.png?imageslim -- 旧版链接带优化参数的
                    所以，下面的操作主要针对于上面的三种情况来处理

                    ***** 所以，这里要改成针对于你自己的文章图片链接来处理 *****
                    
                    """
                    # print('----------------')

                    # 判断图片域名是否为 http://ouej55gp9.bkt.clouddn.com/ 是的话，则替换为 https://qiniu.itfanr.cc
                    if match.startswith('http://ouej55gp9.bkt.clouddn.com'):
                        # 记录下替换前的链接
                        old_url=match
                        new_url = match.replace(
                            'http://ouej55gp9.bkt.clouddn.com', 'https://qiniu.itfanr.cc')
                        # print('step_1_new_url:[{0}]'.format(new_url))

                        # 判断是否以 ?imageslim 结尾
                        if not match.endswith('imageslim'):
                            # 不是，在结尾添加
                            new_url += '?imageslim'
                        
                        print('step_2_new_url:[{0}]'.format(new_url))
                        # 替换 post 中的 old_url为 new_url，并将新内容写回文件
                        new_post = new_post.replace(old_url, new_url)
                        result = True
                    
                    print('----------------')
        if result:
            # 将内容重新写回文件
            # print(new_post)
            md_write(md_file,new_post)
            print('ok-修改成功')
        print('****************')
    
    return result


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
                # break
                pass
            i+=1
        
        time.sleep(2)

    
    print(i)
    


    

if __name__ == '__main__':
    main()

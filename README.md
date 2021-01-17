## md-qiniu-images-replace

### qiniu_img.py

目的：将博客中的 `七牛云临时域名` 图片链接转换为 `个人域名` 链接

#### How to Use

put the `qiniu_img.py` file in directory `your_hexo_dir/source/` ，and then run:

```
$ cd source

$ python qiniu_img.py
```

#### Attention

> 在遍历一遍所有文章包含的图片链接后，发现我的文章中图片链接的特点主要有三种格式：   
>    
> `https://qiniu.itfanr.cc/blog/20180924112100.png?imageslim`  -- 已经符合要求的   
> `http://ouej55gp9.bkt.clouddn.com/blog/20180920204113.png`   -- 只有旧版链接的   
> `http://ouej55gp9.bkt.clouddn.com/blog/180116/B2c2Deah5B.png?imageslim` -- 旧版链接带优化参数的   
> 所以，下面的操作主要针对于上面的三种情况来处理   
> 所以，这里要改成针对于你自己的文章图片链接来处理   
>   

----

### qiniu_img_to_gitee.py

`Update` : 2021-01-17 14:00:35

目的：将博客中的 `七牛云图片` 链接转换为 `Gitee仓库` 中的图片链接

因在七牛云中保存博客图片，导致每月都需要支付 `相对高额` 的 `https流量费` ，而使用私有域名时又需要定期的更换 `https证书` 。遂决定将博客中的七牛云图片链接更换到Gitee中。


#### How to Use

put the `qiniu_img_to_gitee.py` file in directory `your_hexo_dir/source/` ，and then run:

```
$ pip install requests

$ cd source

$ python qiniu_img_to_gitee.py
```

#### Introduction

我的现有博客中的图片链接，主要有以下两种格式：

```
https://qiniu.itfanr.cc/blog/20210116213144.png?imageslim

https://qiniu.itfanr.cc/blog/171117/lggD4efImf.png?imageslim
```

为了更好地管理博客文章中的图片，我在Gitee仓库中设置了一个目录 `blog` 用来单独存储所有的博客图片。


这样，设置的Gitee博客图片路径即为：`https://gitee.com/leafney/blogimage/raw/master/blog/20210117133744.png`


因此，只要将博客中现有图片链接的 `https://qiniu.itfanr.cc` 替换为 `https://gitee.com/leafney/blogimage/raw/master` 即可。


另外，对于某些如 `https://qiniu.itfanr.cc/blog/171117/lggD4efImf.png` 的图片，考虑优化其二级目录，修改为 `https://gitee.com/leafney/blogimage/raw/master/blog/171117lggD4efImf.png` 的格式，即 `Gitee仓库/` + `blog/` + `图片名.png` 的形式。


#### Attention

> 使用时请改成针对于你自己的文章图片链接来处理

----

### qiniu_img_search.py

用于查找markdown文档中的图片链接

----

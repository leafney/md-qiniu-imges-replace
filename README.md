### md-qiniu-images-replace

#### How to Use

put the `qiniu_img.py` file in directory `your_hexo_dir/source/` ，and then run:

```
$ cd source

$ python qiniu_img.py
```

#### Attention

> 在遍历一遍所有文章包含的图片链接后，发现我的文章中图片链接的特点主要有三种格式：   
>    
> https://qiniu.itfanr.cc/blog/20180924112100.png?imageslim  -- 已经符合要求的   
> http://ouej55gp9.bkt.clouddn.com/blog/20180920204113.png   -- 只有旧版链接的   
> http://ouej55gp9.bkt.clouddn.com/blog/180116/B2c2Deah5B.png?imageslim -- 旧版链接带优化参数的   
> 所以，下面的操作主要针对于上面的三种情况来处理   
> 所以，这里要改成针对于你自己的文章图片链接来处理   
>    

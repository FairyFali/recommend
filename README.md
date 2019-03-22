## 推荐系统实例
#### 前言
本项目代码参考于https://github.com/lpty/recommendation.git ，自动动手实现。

#### 环境依赖
+ Python3
    + Pandas,numpy,pickle
+ Sites (演示Demo)
    + Apache + PHP

#### 目录
* 基于协同过滤(UserCF)的模型
* 基于隐语义(LFM)的模型
* 基于图(PersonalRank)的模型

#### 快速开始
请自行下载数据(http://grouplens.org/datasets/movielens/1m)，解压到data/目录中

* 数据预处理

    python read_ratings.py

* 模型运行

    python manage.py [cf/lfm/prank]


#### 参考博客
博客：https://blog.csdn.net/sinat_33741547/article/category/6442592

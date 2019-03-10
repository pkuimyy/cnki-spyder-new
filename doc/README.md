# cnki-spyder-new

### 1. input data 的分析

输入是多个csv文件，在路径 ```/data/input ```下，命名为```[1-9]+_backups.csv```。
每个文件拥有相同的字段，其中比较重要的字段有：

| 字段 |  范例   |
|-|-|
| uname | 牛丽慧 |
| univ | 南京大学 |

### 2. 检索原理

中国知网的检索接口为： http://yuanjian.cnki.com.cn/

在该页面使用 ``` 作者 = uname && 作者单位 = univ ```的检索式进行检索，返回的页面中包含一个文献列表。该文献列表中的每一篇文献都有如下字段：

| 字段 | 范例 |
| - | - |
| 标题 | 纳米出版及其应用研究进展 | 
| 作者 | 牛丽慧 欧石燕 | 
| 关键词 |  纳米出版 语义出版 知识表示 | 
| 期刊 | 《图书情报工作》 | 
| 下载 | 133 | 
| 被引 | 0 |

除了上述在网页上可见的字段以外，还可以从其网页代码中获取如下字段：

| 字段 | 范例 | 其他 |
| - | - | - |
| 文献url | http://www.cnki.com.cn/Article/CJFDTOTAL-TSQB201807022.htm | 可以作为文献的 id |
| 作者url | http://yuanjian.cnki.com.cn/scholar/Result?AuthorFilter=39363873%3b25904869%3b&scholarName=%E7%89%9B%E4%B8%BD%E6%85%A7 | 其中的```AuthorFilter```字段中有所有作者的id，通过字符串```"%3b"```分割|
| 期刊url | http://yuanjian.cnki.com.cn/CJFD/Detail/Index/TSQB | 用于唯一标识一种期刊 | 

备注： 
通过使用作者的id进行检索，可以获得该作者的更多信息，如url：http://yuanjian.cnki.com.cn/scholar/Result?AuthorFilter=39363873 可以获得牛丽慧的更多信息。


### 3. 目标

目标是取得一个csv表格，表格的字段如下：
csv表格用'|'作为分隔符

| 字段 | 范例 |
| - |  - |
| 文献标题 | 纳米出版及其应用研究进展 |
| 文献url |  http://www.cnki.com.cn/Article/CJFDTOTAL-TSQB201807022.htm |
| 作者名 | *见备注 |
| 作者id | *见备注|
| 作者url | http://yuanjian.cnki.com.cn/scholar/Result?AuthorFilter=39363873%3b25904869%3b&scholarName=%E7%89%9B%E4%B8%BD%E6%85%A7 |
| 期刊名 | 《图书情报工作》|
| 期刊url | http://yuanjian.cnki.com.cn/CJFD/Detail/Index/TSQB | 
|下载 | 133 |
| 被引 | 0 |

备注：

作者字符串格式如```"作者id,作者id"```，范例
```"39363873,25904869"```

作者url字符串格式如```"作者姓名,作者姓名"```，范例
```"牛丽慧,欧石燕"```

### 4. 备忘

- 在 input data 中，存在一个学者名对应多个id的情况，
在 output data 中，亦存在一个学者名对应多个id的情况，
重点在于需要一个id匹配的算法，建立input data与 output data中学者id的一一对应关系。
这需要更多的信息，必要的时候需要人手工做。






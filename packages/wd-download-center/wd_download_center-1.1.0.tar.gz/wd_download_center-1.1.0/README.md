##版本说明：
- 5.2.5: add ua list
- 5.2.6: add table create function
- 5.2.7: add ua list again
- 5.2.8: 添加获取百度cookie的方法
- 5.2.9: 修改百度cookie存储位置
- 5.2.10: add *.txt file
- 5.2.11: baidu cookie storage use sorted set
- 5.2.12: add baidu mb cookie
- 5.2.13: 修复本地中文乱码
- 5.2.14: downloader fail
- 5.2.15: downloader fail

#### 新下载中心，2021-08 版
urls参数是一个数组，数组的元素是字符串，字符串的内容是抓取对象的json，抓取对象主要的字段说明
- u，str，请求url
- hs，dict，请求headers
- sleep，int，sleep的秒数，如果有该字段，adsl不进行抓取，仅仅休眠指定的秒数
- debug，是否debug模式 【如果请求时，需要带自定义参数，暂时可以使用此字段】
- et，extract_type，提取类型：0 获取页面 
- - 0->不解析;1->解析百度PC排名结果;2->解析百度移动排名结果;3->解析百度真实URL;
    4->解析百度PC URL是否收录;5->解析360PC排名结果;6->解析360移动排名结果;
    7->解析搜狗PC排名结果;9->解析搜狗移动排名结果;9->解析网页TDK
- cu，cookie_url，cookie的url
- tid，任务id
- uid，请求id，通常是url的md5值
- d，请求的数据，应用自定义的扩展字段 ->测试会报错
- r，redirect，重定向
- v，verify，验证的信息
- ih，is_head
- rh，return header
- rt，retry times，重试次数
- e，encoding，编码方式  
- t，timeout，超时时间，单位秒
- sgg，搜狗微文章的临时url
> 注意:
 - 一般设置tid、uid、u,hs,et字段，其它字段可以不设置
 - 代码要充分利用多线程 服务端是异步
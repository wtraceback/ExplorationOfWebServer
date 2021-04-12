# ExplorationOfWebServer
使用 Python 的 socket 模块编写的一个简易的 web 框架，用于深入理解网络通信及其 Web 应用开发


## 项目结构

```bash
├── db/             # 数据库文件
├── logs/           # log 日记文件
├── models/         # 模型类
├── routes/         # 路由
├── static/         # 静态目录
├── server.py       # 入口文件
└── utils.py        # 封装好的工具函数模块
```


## 项目功能简介
- 请求解析
- 对每个请求都开启一个线程去响应
- 路由处理 - URL 映射
- 响应的封装
- 简易的 cookie 和 session 操作
- md5 + salt 加密密码
- 引入 jinja2 模块渲染模板
- 操作文本文件来充当数据库

- 贯彻 MVC 模式
- 前后端不分离 的 demo - todolist、weibo、blog
- 前后端分离 的 demo - todolist


### server.py
```bash
程序的入口所在
    1. 服务器程序的入口和启动
    2. 开启多线程
        为每一个请求开启一个线程
    3. 请求对象
        实现了一个 Request 类
        解析请求，并封装在 Request 对象中，当做参数传入路由处理函数
    4. 从 route 包中导入各个路由函数模块，组成一个 URL 映射
    5. URL 映射
        URL 和路由处理函数之间的对应关系
            静态路由
            错误路由
            基本的路由函数
```


### models
```bash
数据库包
    1. 编写一个基类
        操作数据库文件中的 保存、读取、查找、删除 等功能
    2. 各个 demo 示例用到的类
```



### routes
```bash
路由函数包
    1. 各个 demo 示例的路由处理函数模块
    2. 全局变量 session
```


### utils
```bash
封装好的工具函数模块
    1. login_required  验证登录权限的装饰器
    2. redirect        重定向函数
    3. current_user    根据 session 来确认当前访问者
    4. http_response   服务器响应函数 - response 相关的信息
    5. render_template 封装好的渲染函数
    6. error           错误响应函数
```

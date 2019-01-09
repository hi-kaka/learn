# -*- coding: utf-8 -*-
#server.py
#从wsgiref模块导入
from wsgiref.simple_server import make_server
#导入我们自己编写的application函数
from helloweb import application

#创建一个http服务，IP为空，端口为8000，处理函数为application
httpd = make_server('',8000,application)
print 'serving http on port 8000........'
httpd.serve_forever()

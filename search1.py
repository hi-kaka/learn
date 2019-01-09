#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-24 15:52:01
# @Author  : kk (zwk.patrick@foxmail.com)
# @Link    : http://blog.csdn.net/PatrickZheng

import os, pdb, logging
logging.basicConfig(level=logging.DEBUG)

def search_dir(path, L):
    current_dir = os.listdir(path)
#    pdb.set_trace()
    for n in current_dir:
#        pdb.set_trace()
        new_path = os.path.join(path, n)
        if os.path.isfile(new_path):  # 需传入路径而非仅仅文件名，否则是FALSE
            logging.debug('%s is a file.' % n)
            L.append(new_path)
        else:
            search_dir(new_path, L)

    return L

def search(s):
    L = search_dir('.', [])

#    pdb.set_trace()
    for file in L: 
#        pdb.set_trace()
        if file.find(s) != -1:
            logging.info('找到包含%s的文件路径：%s' % (s, os.path.abspath(file)))

# os.path.abspath(url) 并非返回url真正完整的绝对路径，只是将当前目录与url进行join操作
# 例如，当前目录为 D:/workplace
# url是 test.txt，实际是在 ./aaa/test.txt
# 但该函数返回的是 D:/workplace/test.txt

if __name__ == '__main__':
    search('test')

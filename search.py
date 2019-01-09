#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def search(name,path='.'):
	if path=='.':
		path = os.path.abspath('.')
	#print 'path : %s' % path
	for i in os.listdir(path):
		if os.path.isfile(os.path.join(path,i)) and name in i:
			print os.path.join(path,i)
		elif os.path.isdir(os.path.join(path,i)):
			search(name,os.path.join(path,i))

def call_search():
	args = sys.argv
	if len(args)==1:
		print 'please enter your arguments'
	else:
		search(args[1])

if __name__=='__main__':
	call_search()

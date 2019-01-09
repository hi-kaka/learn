# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/favicon.ico',methods=['GET'])
def favicon():
	return 'ok'

@app.route('/',methods=['GET','POST'])
def home():
	return render_template('home.html')

@app.route('/signin',methods=['GET'])
def signin_form():
	return render_template('form.html')

@app.route('/signin',methods=['POST'])
def signin():
	#需要从request对象中读取form表单内容做判断
	username = request.form['username']
	password = request.form['password']
	if username=='admin' and password=='password':
		return render_template('sign_ok.html',username=username)
	return render_template('form.html',message='Bad username or password',username=username)

if __name__=='__main__':
	app.run(host='')

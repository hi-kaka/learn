# -*- coding: utf-8 -*-
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	return '''<html>
		  <head>
  		  	<title>Hello</title>
  		  	<style>
    		  		h1 {
      		  			color: #333333;
      		  			font-size: 48px;
      		  			text-shadow: 3px 3px 3px #666666;
    		  		}
  		  	</style>
  		  	<script>
    		  		function change() {
      		  			document.getElementsByTagName('h1')[0].style.color = '#ff0000';
    		  		}
  		  	</script>
		  </head>
		  <body>
  		  	<h1 onclick="change()">Hello, world!</h1>
		  </body>
		  </html>'''

@app.route('/favicon.ico',methods=['GET'])
def favicon():
	return 'test'

@app.route('/signin',methods=['GET'])
def signin_form():
	return '''<form action="/signin" method="post">
		  <p><input name="username"></p>
		  <p><input name="password" type="password"></p>
		  <p><button type="submit">Sign In</button></p>
		  </form>'''

@app.route('/signin',methods=['POST'])
def signin():
	#需要从request对象中读取form表单内容做判断
	if request.form['username']=='admin' and request.form['password']=='password':
		return '<h3>Hello, admin!</h3>'
	return '<h3>Bad username or password.</h3>'

if __name__=='__main__':
	app.run(host='192.168.147.129')

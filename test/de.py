# -*- coding:utf-8 -*-
import nmap
import telnetlib,re
import getpass
#from django.db import models
import os
# from scanhosts.modules import paramiko1_9 as paramiko
# from scanhosts.modules import paramiko2_1_2 as paramiko
import  paramiko
import traceback
#from scanhosts.models import HostLoginifo
#from scanhosts.lib.utils import prpcrypt
import pexpect,datetime

class J_ssh_do(object):
    def __init__(self,info=""):
        self.whitelist = []
        self.result = {"info":info}

    def pass_do(self,login_info,cmd_list=""):
        '''
        用户密码方式登录
        :param login_info:登录的信息，如：('192.168.6.11', 22, 'root', '123')
        :param cmd_list:登录机器后，需要执行的命令
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(login_info[0],login_info[1],login_info[2],login_info[3],timeout=3)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin,stdout,stderr = ssh.exec_command(cmd,timeout=10)
                std_res = stdout.read()
                self.result[cmd] = std_res
        except Exception,e:
            print traceback.print_exc(),login_info
            self.result["status"] = "failed"
            self.result["res"] = str(e)
        finally:
            ssh.close()
        return self.result

    def rsa_do(self,login_info,cmd_list=""):
        '''
        id_rsa密钥登录
        :param login_info:('192.168.6.11', 22, 'root', '/key/id_rsa','123')
        :param cmd_list:
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key = paramiko.RSAKey.from_private_key_file(login_info[3])
            ssh.connect(login_info[0],login_info[1],login_info[2],pkey=key,timeout=2)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin,stdout,stderr = ssh.exec_command(cmd,timeout=10)
            #           stdin.write("Y")   #简单交互，输入 ‘Y’
                std_res = stdout.read()
                self.result[cmd] = std_res
        except Exception as e:
            print traceback.print_exc()
            self.result["status"] = "failed"
            self.result["res"] = e
        finally:
            ssh.close()
        return self.result

    def dsa_do(self,login_info,cmd_list=""):
        '''
        dsa密钥登录
        :param login_info:login_info:('192.168.6.11', 22, 'root', '/key/id_dsa','123')
        :param cmd_list:
        :return:
        '''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key = paramiko.DSSKey.from_private_key_file(login_info[3])
            ssh.connect(login_info[0],login_info[1],login_info[2],pkey=key,timeout=2)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin,stdout,stderr = ssh.exec_command(cmd,timeout=10)
                std_res = stdout.read()
                self.result[cmd] = std_res
        except Exception as e:
            print traceback.print_exc()
            self.result["status"] = "failed"
        finally:
            ssh.close()
        return self.result

    def imoocc_rsa_do(self,login_info,cmd_list=""):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key = paramiko.RSAKey.from_private_key_file(login_info[3], login_info[4])
            ssh.connect(login_info[0],int(login_info[1]),login_info[2],pkey=key,timeout=2)
            self.result["status"] = "success"
            for cmd in cmd_list:
                stdin,stdout,stderr = ssh.exec_command(cmd,timeout=10)
                std_res = stdout.read()
                self.result[cmd] = std_res
        except Exception as e:
            print traceback.print_exc()
            self.result["status"] = "failed"
        finally:
            ssh.close()
        return self.result

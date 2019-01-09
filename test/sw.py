# -*- coding:utf-8 -*-
import os
import re
import telnetlib
import nmap
import time
from de import J_ssh_do
from utils import *

def snmp_begin(nmap_type,ports,password_list,imoocc_key_file,syscmd_list,black_list,s_emails):
    '''
    :param nmap_type:
    :param ports:
    :param password_list:
    :param imoocc_key_file:
    :param imoocc_key_file:
    :param syscmd_list:
    :param black_list:
    :param s_emails:
    :return:
    '''
    if nmap_type is None: return False

    nmap_net = '%s.0/24'%nmap_type
    nm_item = NmapDev(black_list)
    sship_list,host_list,unkown_list = nm_item.nmap_sship(ports,nmap_net)

    key_login_list,key_not_login_list = nm_item.try_key_login(sship_list,imoocc_key_file,syscmd_list)
    canlogin_list,notlogin_list = nm_item.try_login(key_not_login_list,password_list,syscmd_list)
    #nm_item.try_login(key_not_login_list,password_list,syscmd_list)


class NmapDev(object):
    '''
    '''

    def __init__(self,black_list=[]):
        self.black_list = black_list
        self.can_login_lst = {}
        self.not_login_lst = {}
        self.can_key_login_lst = {}
        self.key_not_login_lst = {}

    def nmap_allip(self,nmap_net):
        '''
        '''
        nm = nmap.PortScanner()
        nm.scan(hosts=nmap_net,arguments = ' -n -sP -PE')
        # nm.scan(hosts=nmap_net,arguments = ' -n -PA -PS')
        hostlist = nm.all_hosts()
        return hostlist

    def nmap_sship(self,ports,nmap_net):
        '''
        :param ports:
        :param port_list:
        :param unkown_list:
        :param nmap_net:
        :return:
        '''
        ports = ports
        port_list = ports.split(',')
        nm = nmap.PortScanner()  # 创建端口扫描对象
        ssh_info = {}
        # 调用扫描方法，参数指定扫描主机hosts，nmap扫描命令行参数arguments
        nm.scan(hosts=nmap_net, arguments='-n -sP -PE')
        tcp_all_ip = nm.all_hosts()
        host_list = []
        for ip in tcp_all_ip:  # 遍历扫描主机
            if nm[ip]['status']['state'] == "up":
                 host_list.append(ip)
                 for port in port_list:
                     try:
                         print "Scan ip %s ..... Port %s"%(ip,port)
                         tm = telnetlib.Telnet(host=ip,port=port,timeout=4)
                         tm_res = tm.read_until("\n",timeout=4)
                         if tm_res:
                             if re.search("ssh",tm_res.lower()):
                                 print ip,port
                                 if ip not in self.black_list:
                                     ssh_info[ip]=port
                                     print "[?]IP:%s Port:%s Server:%s"%(ip,port,tm_res)
                     except EOFError as e:
                         pass
                     except Exception as e:
                         pass
        unkown_list = [i for i in host_list if not ssh_info.get(i)]
        print 'ssh_info:', ssh_info
        print 'host_list:', host_list
        print 'unkown_list:', unkown_list
        return ssh_info,host_list,list(set(unkown_list))

    def try_login(self,sship_list,password_list,syscmd_list):
        '''
        尝试ssh用户密码登录，获取机器基本信息
        :param sship_list:
        :param password_list:
        :param syscmd_list:
        :return:
        '''
        password_list = password_list
        syscmd_list = syscmd_list
        if isinstance(sship_list, dict):
            ssh_tuple_list = [(ip,port) for ip,port in sship_list.items()]
        elif isinstance(sship_list,list):
            ssh_tuple_list = sship_list
        for ip,port in ssh_tuple_list:
            #system_info = ""
            for password in password_list:
                if ip not in self.can_login_lst.keys():
                    login_info = (ip,int(port),'root', password)
                    doobj = J_ssh_do(login_info)
                    res = doobj.pass_do(login_info,syscmd_list)
                    if res["status"] == "success":
                        if self.not_login_lst.has_key(ip):
                            self.not_login_lst.pop(ip)
                        sys_hostname = res["hostname"]
                        sys_mac = mac_trans(res["cat /sys/class/net/[^vtlsb]*/address||esxcfg-vmknic -l|awk '{print $8}'|grep ':'"])
                        sys_sn = sn_trans(res["dmidecode -s system-serial-number"])
                        system_info = getsysversion([res["cat /etc/issue"],res["cat /etc/redhat-release"]])
                        machine_type = machine_type_trans(res["dmidecode -s system-manufacturer"] + res["dmidecode -s system-product-name"])
                        print "ssh login and exec command:%s"%res
                        self.can_login_lst[ip] = (port,password,'root',system_info,sys_hostname,sys_mac,sys_sn,machine_type)
                    elif res["status"] == "failed" and re.search(r"reading SSH protocol banner",res["res"]):
                        # print "res res..........................",res['res']
                        #print "IP:%s Connection closed by remote host,Sleep 60 (s).................. "%ip,res
                        print "%s:%s:%s paramiko banner_timeout too short or server's sshd not response (%s).................. "%ip,port,password,res
                        #time.sleep(60)
                    else:
                        if ip not in self.not_login_lst.keys() and ip not in self.can_login_lst.keys():
                            self.not_login_lst[ip] = port
                        # print ip,port,password,traceback.print_exc()
        print 'self.can_login_lst:', self.can_login_lst
        print 'self.not_login_lst:', self.not_login_lst
        return self.can_login_lst,self.not_login_lst

    def try_key_login(self,sship_list,allkeyfile,syscmd_list):
        '''
        尝试ssh秘钥登录，获取机器基本信息
        :param sship_list:
        :param allkeyfile:
        :param syscmd_list:
        :return:
        '''

        # import traceback
        for ip,port in sship_list.items():
            print "try key login....",ip,port
            keyfile = allkeyfile[0]
            if ip not in self.can_key_login_lst.keys():
                print 'try idrsakey....',ip,port,keyfile
                login_info = (ip,int(port),'root',keyfile)
                doobj = J_ssh_do(login_info)
                res = doobj.rsa_do(login_info,syscmd_list)
                if res["status"] == "success":
                    sys_hostname = res["hostname"]
                    system_info = getsysversion([res["cat /etc/issue"],res["cat /etc/redhat-release"]])
                    sys_mac = mac_trans(res["cat /sys/class/net/[^vtlsb]*/address||esxcfg-vmknic -l|awk '{print $8}'|grep ':'"])
                    sys_sn = sn_trans(res["dmidecode -s system-serial-number"])
                    machine_type = machine_type_trans(res["dmidecode -s system-manufacturer"] + res["dmidecode -s system-product-name"])
                    self.can_key_login_lst[ip] = (port,keyfile,"root","",1,system_info,sys_hostname,sys_mac,sys_sn,machine_type)
                if res["status"] == "failed":
                        keyfile = allkeyfile[1]
                        print "try iddsa login...",ip,port,keyfile
                        login_info = (ip,port,'root', keyfile)
                        doobj = J_ssh_do(login_info)
                        res = doobj.dsa_do(login_info,syscmd_list)
                        if res["status"] == "success":
                            sys_hostname = res["hostname"]
                            system_info = getsysversion([res["cat /etc/issue"],res["cat /etc/redhat-release"]])
                            sys_mac = mac_trans(res["cat /sys/class/net/[^vtlsb]*/address||esxcfg-vmknic -l|awk '{print $8}'|grep ':'"])
                            sys_sn = sn_trans(res["dmidecode -s system-serial-number"])
                            machine_type = machine_type_trans(res["dmidecode -s system-manufacturer"] + res["dmidecode -s system-product-name"])

                            if self.key_not_login_lst.has_key(ip):self.key_not_login_lst.pop(ip)
                            self.can_key_login_lst[ip] = (port,keyfile,"root","",2,system_info,sys_hostname,sys_mac,sys_sn,machine_type)
                        else:
                            keyfile = allkeyfile[2]
                            print "try Non-root idrsa login...",ip,port
                            password = '0koooAdmin'
                            login_info = (ip,port,'imoocc', keyfile,password)
                            doobj = J_ssh_do(login_info)
                            res = doobj.imoocc_rsa_do(login_info,syscmd_list)
                            if res["status"] == "success":
                                sys_hostname = res["hostname"]
                                sys_mac = mac_trans(res["cat /sys/class/net/[^vtlsb]*/address||esxcfg-vmknic -l|awk '{print $8}'|grep ':'"])
                                system_info = getsysversion([res["cat /etc/issue"],res["cat /etc/redhat-release"]])
                                sys_sn = sn_trans(res["dmidecode -s system-serial-number"])
                                machine_type = machine_type_trans(res["dmidecode -s system-manufacturer"] + res["dmidecode -s system-product-name"])
                                if self.key_not_login_lst.has_key(ip):self.key_not_login_lst.pop(ip)
                                self.can_key_login_lst[ip] = (port,keyfile,"imoocc","",3,system_info,sys_hostname,sys_mac,sys_sn,machine_type)
                            else:
                                if ip not in self.key_not_login_lst.keys() and ip not in self.can_key_login_lst.keys():
                                    self.key_not_login_lst[ip] = port
        print 'self.can_key_login_lst:', self.can_key_login_lst
        print 'self.key_not_login_lst:', self.key_not_login_lst
        return  self.can_key_login_lst,self.key_not_login_lst

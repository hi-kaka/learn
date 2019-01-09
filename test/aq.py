# -*- coding:utf-8 -*-
import datetime
import os
import re
import yaml
import time
from sw import snmp_begin

def main():
    '''
    读取扫描所需配置文件
    :return:
    '''
    s_conf = yaml.load(file('./scanhosts.yaml'))
    s_nets = s_conf['hostsinfo']['nets']
    s_ports = s_conf['hostsinfo']['ports']
    s_pass = s_conf['hostsinfo']['ssh_pass']
    s_cmds = s_conf['hostsinfo']['syscmd_list']
    s_keys = s_conf['hostsinfo']['ssh_key_file']
    s_blacks = s_conf['hostsinfo']['black_list']
    s_emails = s_conf['hostsinfo']['email_list']

    n_sysname_oid = s_conf['netinfo']['sysname_oid']
    n_sn_oid = s_conf['netinfo']['sn_oids']
    n_commu = s_conf['netinfo']['community']
    n_login_sw = s_conf['netinfo']['login_enable']
    n_backup_sw = s_conf['netinfo']['backup_enable']
    n_backup_sever = s_conf['netinfo']['tfp_server']

    d_pass = s_conf['dockerinfo']['ssh_pass']
    starttime = datetime.datetime.now()
    # '''
    # 扫描主机信息
    # '''
    for nmap_type in s_nets:
        #unkown_list,key_not_login_list = snmp_begin(nmap_type,s_ports,s_pass,s_keys,s_cmds,s_blacks,s_emails)
        snmp_begin(nmap_type,s_ports,s_pass,s_keys,s_cmds,s_blacks,s_emails)

if __name__ == '__main__':
    main()

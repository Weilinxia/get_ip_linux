#!/usr/bin/env python
import re
import subprocess
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = ""      # SMTP服务器
mail_user = ""      # 用户名
mail_pass = ""      # 授权密码，非登录密码

sender = ''       # 发件人邮箱
receivers = ['']  # 接收邮箱

content = 0
title = 'My IP has changed'  # 邮件主题

#这个函数用于读取当前系统的静态ipv6地址（只适用于单网卡，如果你有很多个静态ipv6地址，请重新编写正则表达式）
def get_ip():
    ips = subprocess.getoutput('ip -6 addr')         #这是一个 iproute2util 中的命令，你可能需要安装它
    pattern = re.compile(r'(?<=inet6 ).*(?=/64 scope global d)')    #这是一个正则表达式，你可以根据你的系统情况来编写或者询问作者
    ips_1 = pattern.findall(ips)
    ips_2 =''.join(ips_1)
    return ips_2

#这个函数查询ip记录是否创建，没有则创建它并返回true；有记录则对比记录ip，相同则返回false，不同则返回ture
def ip_compare(ip_addr):
    ip_temp_path = "/home/ip.txt"  #记录ip的文件地址
    if not os.path.exists(ip_temp_path):
        f = open(ip_temp_path, 'w')
        f.write(ip_addr)
        f.close()
        return True
    else:
        f = open(ip_temp_path, 'r')
        origin_ip = f.read()
        f.close()
        if origin_ip == ip_addr:
            return False
        else:
            f = open(ip_temp_path, 'w')
            f.write(ip_addr)
            f.close()
            return True

#这是一个邮件发送函数，网络上资料很多
def sendEmail(ip_addr):

    message = MIMEText(ip_addr, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


ip_addr=get_ip()
if ip_compare(ip_addr):
    sendEmail(ip_addr)
else:
    pass

     
     
     
     
     
     

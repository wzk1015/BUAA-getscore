#coding=utf-8
'''
使用说明：使用前先根据你的情况修改部分代码，修改好后保存然后双击就进入运行状态了。要保持本脚本可以正常运行，需要保持网络正常、脚本窗口不关闭。如果想停止接收邮件，关闭该窗口即可。
首先需要选择用于发送成绩信息的邮箱，需要在邮箱提供商处设置开启SMTP，并将SMTP服务器、发件邮箱用户名、发件邮箱密码依次替换send_mail函数的对应内容
然后选择用于收件的邮箱（可与发件邮箱相同），替换对应内容
最后需要获取Cookie。Chrome的获取方法：在浏览器中打开https://app.buaa.edu.cn/buaascore/wap/default/index，并用自己的统一认证账号登录，然后按下F12进入开发者模式，在最上面一栏中点"Application"，在左边栏点"Cookies"左边的小三角，选中"Cookies"下第一个项，将每个元素的名称和值按'Name':'Value'的格式填入代码中的cookies，也就是把cookies建立成由【名称到值的映射】构成的字典

'''
import re
import requests
import os
import time
from html.parser import HTMLParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail(title,content):
    # 第三方 SMTP 服务
    mail_host=""  #设置SMTP服务器，如smtp.qq.com
    mail_user=""    #发送邮箱的用户名，如xxxxxx@qq.com
    mail_pass= ""  #发送邮箱的密码（注：QQ邮箱需要开启SMTP服务后在此填写授权码）
    sender = mail_user #发件邮箱，如xxxxxx@qq.com
    receivers = ""   # 收件邮箱，格式同发件邮箱

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')#发件人
    message['To'] =  Header(receivers, 'utf-8')#收件人
    subject = title#主题
    message['Subject'] = Header(subject, 'utf-8')
    print('Prepare success')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        print('Connect success')
        smtpObj.login(mail_user,mail_pass)
        print('Login success')
        smtpObj.sendmail(sender, receivers, str(message))
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print("ERROR：无法发送邮件")

url=r"https://app.buaa.edu.cn/buaascore/wap/default/index"
cookies={  # 以下是示例。用你的cookie替换
'xxbh21.8' : '',
'eai-sess' : '',
'_ga' : '',
'UUkey' : '',
'Hm_lvt_8edeba7d3ae859d72148a873531e0fa5': '',
'Hm_lpvt_8edeba7d3ae859d72148a873531e0fa5': '',
'_webvpn_key' : '',
'webvpn_username' : ''    
}

def send_gpa():
    global gpa
    title='出分啦！你的GPA变为 '+gpa
    content='你当前的GPA：'+gpa+'\n快去教务网看你的成绩！'
    send_mail(title,content)

def check_gpa(init = True):
    global gpa
    st=webstr.find('gpa:')
    ed=webstr.find('\n',st)
    newgpa = webstr[st+5:ed-1]
    if gpa == 0:
        gpa = newgpa
        print(gpa, "初始化")
        if init:
            send_gpa()
    elif gpa[0] != "3":
        print("ERR HTML")
    elif gpa != newgpa:
        gpa = newgpa
        print("出分啦!!!!!!!!!!!GPA变为", gpa)
        send_gpa()
    else:
        print(gpa,"no update")

if __name__ == "__main__":
    gpa = 0
    while True:
        print(time.ctime())
        try:
            r=requests.get(url,headers={'User-agent':'Mozilla 5.10'},cookies=cookies)
        except:
            time.sleep(60)
            continue
        r.encoding='utf8'
        f1=open("html.txt","w")
        webstr=r.text.encode('gbk','ignore').decode('gbk')
        f1.write(webstr)
        f1.close()
        #print("code =",r.status_code)
        check_gpa(False)
        time.sleep(60)
    
        
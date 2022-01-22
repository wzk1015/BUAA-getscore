'''
使用说明：使用前先根据你的情况修改部分代码，修改好后保存然后双击就进入运行状态了。要保持本脚本可以正常运行，需要保持网络正常、脚本窗口不关闭。如果想停止接收邮件，关闭该窗口即可。
首先需要选择用于发送成绩信息的邮箱，需要在邮箱提供商处设置开启SMTP，并将SMTP服务器、发件邮箱用户名、发件邮箱密码依次替换19-21行的对应内容，并用发件邮箱的地址替换22行的对应内容
然后选择用于收件的邮箱（可与发件邮箱相同），替换23行的对应内容（如果有多个收件人，需要用List保存各个收件人的邮箱地址并用该List替换）
最后需要获取Cookie。Chrome的获取方法：在浏览器中打开https://app.buaa.edu.cn/buaascore/wap/default/index，并用自己的统一认证账号登录，然后按下F12，在最上面一栏中点"Application"，在左边栏点"Cookies"左边的小三角，选中"Cookies"下第一个项，将每个元素的名称和值按'Name':'Value'的格式填入代码中的cookies，也就是把cookies建立成由【名称到值的映射】构成的字典

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
    mail_host="SMTPServer"  #设置SMTP服务器，如smtp.qq.com
    mail_user="YourEmailAccount"    #发送邮箱的用户名，如xxxxxx@qq.com
    mail_pass= "YourEmailPassword"  #发送邮箱的密码（注：QQ邮箱需要开启SMTP服务后在此填写授权码）
    sender = 'YourSenderEmail' #发件邮箱，如xxxxxx@qq.com
    receivers = 'YourReceiverEmail'   # 收件邮箱，格式同发件邮箱

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
cookies={  # 用你的cookie替换

}
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
    print("code=",r.status_code)
    st=webstr.find('list: ')
    ed=webstr.find('\n',st)
    scorestr=webstr[st:ed]
    st=webstr.find('gpa:')
    ed=webstr.find('\n',st)
    gpa=webstr[st+5:ed-1]
    st,ed=0,0
    scorelist=[]
    try:
        f2=open('scorelist.txt','r')
        courseinfo=f2.readlines()
        f2.close()
    except:
        courseinfo=[]
    coursename=[]
    for coursedict in courseinfo:
        coursename.append(eval(coursedict)['kcmc'])
    newlist=[]
    flag=False
    while True:
        st=scorestr.find('{',st+1)
        ed=scorestr.find('}',ed+1)
        if st==-1 or ed==-1:
            break
        subdict=eval(scorestr[st:ed+1])
        scorelist.append(subdict)
        try:
            coursename.index(subdict['kcmc'])
        except:#send notification
            newlist.append((subdict['kcmc'],subdict['kccj']))
            flag=True
    if flag:
        title='出分啦！你的GPA变为 '+gpa
        content='你当前的GPA：'+gpa+'\n新出分的课程：\n'
        for (name,score) in newlist:
            content+=name+'\t分数：'+score+'\n'
        content+='\n所有已出成绩课程信息如下：\n'
        for i in range(len(scorelist)):
            content+=scorelist[i]['kcmc']+'\t分数：'+scorelist[i]['kccj']+'\t分数类型：'+scorelist[i]['fslx']+'\t学分：'+scorelist[i]['xf']+'\t课程类型：'+scorelist[i]['kclx']+'\n'
        send_mail(title,content)
    f2=open('scorelist.txt','w')
    for dic in scorelist:
        f2.write(str(dic)+'\n')
    f2.close()
    time.sleep(60)
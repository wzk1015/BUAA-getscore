## 北航成绩查询脚本

标题党了，其实是很早前的一个查分脚本，感谢[@ViYulton](https://github.com/ViYulton)提供的版本（`ScoreGet_ReleasedVersion_v1.1.py`，~~这个版本可能更好因为能记录成绩列表~~），我改的简（ruo）洁（zhi）了一些。



### 功能

每分钟刷新本学期GPA，若发生变化（即有课程出分）则一分钟内自动发送邮件至邮箱。手机上安装邮箱app即可保证实时收到提醒。



### 使用方法

1. 选择用于发送成绩信息的邮箱，需要在邮箱提供商处设置开启SMTP，并将SMTP服务器、发件邮箱用户名、发件邮箱密码依次替换send_mail函数的对应内容
2. 选择用于收件的邮箱（可与发件邮箱相同），替换对应内容
3. 获取Cookie。Chrome的获取方法：在浏览器中打开[查分网址](https://app.buaa.edu.cn/buaascore/wap/default/index)，并用自己的统一认证账号登录，然后按下F12进入开发者模式，在最上面一栏中点"Application"，在左边栏点"Cookies"左边的小三角，选中"Cookies"下第一个项，将每个元素的名称和值按`'Name':'Value'`的格式填入代码中的cookies，也就是把cookies建立成由【名称到值的映射】构成的字典
4. 运行`getscore.py`



注：需要保证**py程序持续运行**才能发送邮件。有服务器的话可以挂到服务器后台上运行。

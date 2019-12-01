#  南昌大学分数更新提示系统


主要功能:

通过模拟登录、爬虫每隔3分钟访问南昌大学教务管理系统并获取成绩表,并保存到本地.如果某一次获取的成绩与上一次获取的成绩有所差异,就将新的成绩发送至预先指定的邮箱当中,以此起到分数更新提醒的作用.

使用到的第三方库:

requests

BeautifulSoup

pytesseract

PIL

其中pytesseract库需要tesseract-OCR软件的支持,此处提供Windows版的下载链接:

https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-setup-3.02.02.exe/download

理论上说,只要确保第三方库全部成功安装,并且也安装了tesseract-OCR软件和设置其到PATH中,就可以正常使用了.

具体使用方法:

确保你的QQ邮箱已经开启了SMTP服务(不知道如何开启请自行百度)->填写好emailsend.py文件中的邮箱和授权码到函数变量中->保存好修改后的代码->到下载到本地的代码目录运行命令行->运行python main.py

大功告成!

----
2019.12.1更新

更换了访问的url,现在能够正常使用了

发布了GUI版本的exe文件,可以直接下载使用,脱离python环境依赖

更新了验证码的OCR识别
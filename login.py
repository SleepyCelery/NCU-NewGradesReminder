import requests
import base64
from VerifyCode import recognize
from DataMatch import datamatch
from bs4 import BeautifulSoup
import time


def convert(username, password):  # 将账号和密码通过base64编码和拼接作为登录的formdata
    encoded = base64.b64encode(username.encode()).decode() + '%%%' + base64.b64encode(password.encode()).decode()
    return encoded


def findVerifyCode(text):  # 从返回的网页源代码中获取到验证码的url
    soup = BeautifulSoup(text, 'html.parser')
    url = soup.find('img', attrs={'id': 'SafeCodeImg'})['src']
    url = "http://218.64.56.18" + url
    return url


def searchquestion(text):  # 根据提交登陆表单之后返回的网页源代码来判断验证码是否存在问题
    try:
        soup = BeautifulSoup(text, 'html.parser')
        return soup.find('font', attrs={'color': "red"}).string
    except AttributeError:
        return ""


def getgrades(username, password):
    while True:
        jwglxt = requests.Session()  # 构建一个Session类用来访问教务管理系统
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': '218.64.56.18',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }  # 构建Headers
        login = jwglxt.get(url='http://218.64.56.18/jsxsd/xsxk/xklc_list?Ves632DSdyV=NEW_XSD_PYGL#', headers=headers)
        login.encoding = login.apparent_encoding
        img = jwglxt.get(findVerifyCode(login.text))  # 获取验证码
        with open('verify.jpg', mode='wb') as code:
            code.write(img.content)
            code.close()
        safecode = str(recognize('verify.jpg'))  # 调用函数识别验证码
        if safecode == "":
            print("验证码识别失败,等待3秒后重新获取验证码!")
            time.sleep(3)
            continue
        post_data = {
            'encoded': convert(username, password),
            'RANDOMCODE': safecode
        }  # 构建登陆表单
        firstpage = jwglxt.post(url='http://218.64.56.18/jsxsd/xk/LoginToXk', data=post_data)
        firstpage.encoding = firstpage.apparent_encoding
        tips = searchquestion(firstpage.text)  # 登录教务管理系统的进程到此为止,后面的代码属于判断
        if tips == "":  # 如果登录没有问题,就获取成绩表
            cj = jwglxt.post(url='http://218.64.56.18/jsxsd/kscj/cjcx_list',
                             data={'kksj': '', 'kcxz': '', 'kcmc': '', 'xsfs': 'all'})
            cj.encoding = cj.apparent_encoding  # 此处由于需要302重定向,为了跨域保存cookie,故不分函数,直接将获取成绩表的功能写入函数
            with open(username, 'w', encoding='utf-8') as file:
                file.write(cj.text)
                file.close()
            print("已获取到最新成绩!")
            return datamatch(username)
        elif tips == '验证码错误!!':  # 登录出现问题,就重复上面的所有过程
            print('自动填写验证码出错,等待5秒重新获取成绩!')
            time.sleep(5)
        elif tips == '用户名或密码错误':
            print('用户名或密码错误!请退出本程序后重新输入!')
            print('将在10秒钟后自动退出程序!')
            time.sleep(10)

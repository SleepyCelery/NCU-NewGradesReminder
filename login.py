import base64
import time
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from DataMatch import datamatch
from VerifyCode import recognize


def convert(username, password):  # 将账号和密码通过base64编码和拼接作为登录的formdata
    encoded = base64.b64encode(username.encode()).decode() + '%%%' + base64.b64encode(password.encode()).decode()
    return encoded


def findVerifyCode(text):  # 从返回的网页源代码中获取到验证码的url
    soup = BeautifulSoup(text, 'html.parser')
    url = soup.find('img', attrs={'id': 'SafeCodeImg'})['src']
    url = "http://jwc104.ncu.edu.cn:8081" + url
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
            'Host': 'jwc104.ncu.edu.cn:8081',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }  # 构建Headers
        login = jwglxt.get(url='http://jwc104.ncu.edu.cn:8081/jsxsd/', headers=headers)
        # print('Get net info successfully!')
        login.encoding = login.apparent_encoding
        img = jwglxt.get(findVerifyCode(login.text))  # 获取验证码
        # print('Get verify code successfully!')
        safecode = str(recognize(BytesIO(img.content), priority='baidu'))  # 调用函数识别验证码
        if safecode == "":
            print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
            print("验证码识别失败,等待1秒后重新获取验证码!")
            time.sleep(1)
            continue
        post_data = {
            'encoded': convert(username, password),
            'RANDOMCODE': safecode
        }  # 构建登陆表单
        firstpage = jwglxt.post(url='http://jwc104.ncu.edu.cn:8081/jsxsd/xk/LoginToXk', data=post_data)
        # print('Log in successfully!')
        firstpage.encoding = firstpage.apparent_encoding
        tips = searchquestion(firstpage.text)  # 登录教务管理系统的进程到此为止,后面的代码属于判断
        if tips == "":  # 如果登录没有问题,就获取成绩表
            cj = jwglxt.post(url='http://jwc104.ncu.edu.cn:8081/jsxsd/kscj/cjcx_list',
                             data={'kksj': '', 'kcxz': '', 'kcmc': '', 'xsfs': 'all'})
            cj.encoding = cj.apparent_encoding  # 此处由于需要302重定向,为了跨域保存cookie,故不分函数,直接将获取成绩表的功能写入函数
            print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
            print("已获取到最新成绩!")
            return datamatch(cj.text)
        elif tips == '验证码错误!!':  # 登录出现问题,就重复上面的所有过程
            print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
            print('自动填写验证码出错,等待1秒重新获取成绩!')
            time.sleep(1)
        elif tips == '用户名或密码错误':
            print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
            print('用户名或密码错误!请退出本程序后重新输入!')
            print('[{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), end='')
            print('将在10秒钟后自动退出程序!')
            time.sleep(10)
            exit()

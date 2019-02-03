import time
from gradesjudge import gradesjudge
from emailsend import emailsend, buildtext
from pytesseract import TesseractError
from requests import ConnectionError
from smtplib import SMTPConnectError

if __name__ == '__main__':
    print('--------------------南昌大学分数更新提示系统--------------------')
    print('Powered by ChaoYihu, Data from 南昌大学教务管理系统')
    username = input('请输入学号:')
    password = input('请输入密码:')
    email = input('请输入获取提示邮件的邮箱(推荐使用QQ邮箱,example@qq.com):')
    while True:
        try:
            waitsend = gradesjudge(username, password)
            if waitsend is None:
                print('等待3分钟后重新获取新数据...')
                time.sleep(180)
            else:
                emailsend(buildtext(username, waitsend), email)
                print('等待3分钟后重新获取新数据...')
                time.sleep(180)
        except TesseractError:
            print('系统出错!请检查是否安装Tesseract-OCR并将其置于环境变量PATH!')
            print('等待1分钟后重新获取新数据...')
            time.sleep(60)
        except ConnectionError:
            print('系统出错!请检查网络是否通畅!')
            print('等待1分钟后重新获取新数据...')
            time.sleep(60)
        except SMTPConnectError:
            print('系统出错!请检查邮箱地址和授权码是否填写正确!')
            print('等待1分钟后重新获取新数据...')
            time.sleep(60)

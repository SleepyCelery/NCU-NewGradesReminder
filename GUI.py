'''
GUI应该包含六个输入框,分别为学号 密码 发送邮箱 邮箱smtp服务器host 邮箱地址 邮箱token
包含三个按钮,分别为载入配置 写入配置 和 开始监视
包含一个状态显示栏,所有消息均显示在该栏中
'''

from tkinter import *

if __name__ == '__main__':
    root = Tk()
    root.title = '南昌大学分数更新提示系统'
    root.wm_title
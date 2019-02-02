#  通过学号和密码获取到成绩列表之后,再与先前获取到的成绩进行比较,如果有新的成绩,就组织格式发送到提示邮箱,如果没有新的成绩,就提示无新成绩.
#  要求做文件是否存在的判断
from login import getgrades
import os
import json


def gradesjudge(username, password):
    tail = '_list.json'
    newgrades = getgrades(username, password)
    waitsend = {}
    if os.path.exists(username + tail):
        with open(username + tail, mode='r', encoding='utf-8') as cjold:
            oldgrades = json.load(cjold)
            cjold.close()
        for i in newgrades.keys():
            if i not in oldgrades.keys():
                waitsend[i] = newgrades[i]
        if waitsend == {}:
            print('无新成绩可保存!')
            return None
        else:
            with open(username + tail, mode='w', encoding='utf-8') as cjnew:
                json.dump(newgrades, cjnew)
                cjnew.close()
            print('已保存新成绩!')
            return waitsend
    else:
        for i in newgrades.keys():
            waitsend[i] = newgrades[i]
        with open(username + tail, mode='w', encoding='utf-8') as cjnew:
            json.dump(newgrades, cjnew)
            cjnew.close()
        print('已保存新成绩!')
        return waitsend

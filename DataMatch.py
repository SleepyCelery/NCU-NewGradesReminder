from bs4 import BeautifulSoup


def datamatch(path):  # 匹配出来的结果 第一项序号 第二项学期 第三项学科编号 第四项学科名称 第五项成绩 第六项学分 第七项学时 第八项考核方式 第九项学科要求
    with open(path, "r", encoding="UTF-8") as file:
        content = file.read()
        file.close()
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find_all("td")
    allinfo = []
    info = []
    count = 0
    datadic = {}
    for i in results[1:]:
        if count < 9:
            info.append(i.string)
            count += 1
        else:
            allinfo.append(info)
            info = []
            count = 0
    info = []
    for i in allinfo:
        datadic[i[3]] = i[4]

    return datadic

    # 匹配出来的结果 第一项序号 第二项学期 第三项学科编号 第四项学科名称 第五项成绩 第六项学分 第七项学时 第八项考核方式 第九项学科要求


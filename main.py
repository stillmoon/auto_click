import datetime
import json
import os
import pathlib
import random
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import requests as requests


def send_mail(recv, title, content, file=None):
    """
    发送邮件函数，默认使用163smtp
    :param content: 正文
    :param recv: 邮箱接收人地址，多个账号以逗号隔开
    :param title: 邮件标题
    :param file: 附件
    :return:
    """
    # localtime = time.localtime(time.time())
    # date = '%d-%02d-%02d' % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
    # now_time = ' %02d:%02d' % (localtime.tm_hour, localtime.tm_min)
    # detail_time = date + now_time
    now = datetime.datetime.now()
    now = now + datetime.timedelta(hours=0)
    detail_time = now.strftime('%Y-%m-%d %H:%M:%S')

    username = 'xxxxxx@qq.com'  # 邮箱账号
    passwd = 'xxxxxxxxx'  # 邮箱密码
    recv = recv + '@qq.com'
    # content = detail_time + content  # 加上时间戳
    mail_host = 'smtp.qq.com'  # 邮箱服务器
    port = 465  # 端口号

    # # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
    # # file_handle.writelines(detail_time + '\n发送给' + recv + title + ' 正在进行\n')
    # # file_handle.writelines('——————————————————\n')
    # # file_handle.close()
    print(detail_time + '\n发送给' + recv + title + ' 正在进行')
    print('——————————————————')

    if file:
        msg = MIMEMultipart()
        # 构建正文
        part_text = MIMEText(content, 'utf-8')
        msg.attach(part_text)  # 把正文加到邮件体里面去

        # 构建邮件附件
        part_attach1 = MIMEApplication(open(file, 'rb').read())  # 打开附件
        part_attach1.add_header('Content-Disposition', 'attachment', filename=pathlib.Path(file).name)  # 为附件命名
        msg.attach(part_attach1)  # 添加附件
    else:
        msg = MIMEText(content, 'html', 'utf-8')  # 邮件内容

    msg['Subject'] = title  # 邮件主题
    msg['From'] = username  # 发送者账号
    msg['To'] = recv  # 接收者账号列表

    count = 0
    while True:
        try:
            if count > 3:
                break

            smtp = smtplib.SMTP_SSL(mail_host, port=port)
            smtp.connect(mail_host, port=port)
            smtp.login(username, passwd)  # 登录
            smtp.sendmail(username, recv, msg.as_string())
            smtp.quit()

        except (smtplib.SMTPException or TimeoutError) as err:
            now = datetime.datetime.now()
            now = now + datetime.timedelta(hours=0)
            detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
            # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
            # file_handle.writelines(detail_time + '\n发送给' + recv + title + ' is failed\n')
            # file_handle.writelines(str(err) + '\n')
            # file_handle.writelines('——————————————————\n')
            # file_handle.close()
            print(detail_time + '\n发送给' + recv + title + ' is failed')
            print(str(err))
            print('——————————————————')
            sleep(3)
            count += 1
            continue

        now = datetime.datetime.now()
        now = now + datetime.timedelta(hours=0)
        detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
        # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
        # file_handle.writelines(detail_time + '\n发送给' + recv + title + ' is succeed\n')
        # file_handle.writelines('——————————————————\n')
        # file_handle.close()
        print(detail_time + '\n发送给' + recv + title + ' is succeed')
        print('——————————————————')
        break


def daka(data):
    now = datetime.datetime.now()
    now = now + datetime.timedelta(hours=0)
    url = 'https://ehallplatform.xust.edu.cn/default/jkdk/mobile/com.primeton.eos.jkdk.xkdjkdkbiz.jt.biz.ext'
    num = 1
    jdlx = "0"     #晨午检打卡标志
    if now.strftime("%H:%M") < "18:00":
        num = 0
        jdlx = "1"
    delta = datetime.timedelta(days=num)
    print("jdlx==============" + jdlx)

    uid = data.get("uid")       # UID
    empid = data.get("empid")       # ID号
    jrrq1 = (now + delta).strftime('%Y-%m-%d')      # 打卡时间
    sjh2 = data.get("sjh2")     # 手机号
    jrsfzx3 = data.get("jrsfzx3")       # 是否在校 “是”\“否”
    sheng = data.get("sheng")       # 省
    shi = data.get("shi")       # 市
    xian = data.get("xian")     # 县（区）
    szdd4 = "中国" + sheng + shi + xian   # 大体地址
    xxdz41 = data.get("xxdz41")     # 详细地址
    gh = data.get("gh")     # 学号
    xm = data.get("xm")     # 姓名
    xb = data.get("xb")     # 性别
    # jd = random.uniform(109.19, 109.20)
    # jingdu = '%.05f' % round(jd, 5)
    jingdu = data.get("jinngdu") + "%03d" % random.randint(0, 999)      # 地址精度
    # wd = random.uniform(34.36, 34.37)
    # weidu = '%.05f' % round(wd, 5)
    weidu = data.get("weidu") + "%03d" % random.randint(0, 999)     # 地址纬度
    tbsj = now.strftime('%Y-%m-%d %H:%M:%S')        # 提交详细时间
    time = now.strftime('%Y-%m-%d')     # 提交时间

    jsons = {
        "xkdjkdk": {
            "procinstid": "",
            "empid": empid,
            "shzt": "-2",
            "id": "",
            "jrrq1": jrrq1,
            "sjh2": sjh2,
            "jrsfzx3": jrsfzx3,
            "szdd4": szdd4,
            "xxdz41": xxdz41,
            "jrtwfw5": "正常体温:36～37.2℃",
            "jrsfjgwh6": "否",
            "jrsfjghb7": "否",
            "jrsfcxfrzz8": "否",
            "jrsfywhrjc9": "否",
            "jrsfyhbrjc10": "否",
            "jrsfjcgrrq11": "否",
            "jssfyqzysgl12": "否",
            "sfcyglq13": "否",
            "glkssj131": "",
            "gljssj132": "",
            "sfyyqxgzz14": "否",
            "qtxx15": None,
            "gh": gh,
            "xm": xm,
            "xb": xb,
            "sfzh": "",
            "szyx": "xxxxx",        # 学院全称
            "xydm": "4007",
            "zy": "",
            "zydm": "",
            "bj": "xxxxxx",   # 班级
            "bjdm": "xxxxxx",   # 班级代码
            "jg": "",
            "yx": "",
            "sfxs": "是",
            "xslx": "1",
            "jingdu": jingdu,
            "weidu": weidu,
            "guo": "中国",
            "sheng": sheng,
            "shi": shi,
            "xian": xian,
            "sfncxaswfx16": "否",
            "dm": "xxxxx",  # 班级代码
            "jdlx": jdlx,
            "tbsj": tbsj,
            "fcjtgj17Qt": "",
            "fcjtgj17": "",
            "hqddlx": "1",
            "ymtys": "",
            "time": time
        }
    }

    # print(jsons)
    # try:
    if True:
        session = requests.session()
        session.get(
            url='https://ehallplatform.xust.edu.cn/default/jkdk/mobile/mobJkdkAdd_test.jsp?uid'
                '=' + uid, verify=False)
        respond = session.post(url=url, json=jsons, verify=False)
        if respond.json().get('exception') is None:
            now = datetime.datetime.now()
            now = now + datetime.timedelta(hours=0)
            detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
            # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
            # file_handle.writelines(detail_time + f'\n{data["xm"]}打卡成功\n')
            # file_handle.writelines('——————————————————\n')
            # file_handle.close()
            print(detail_time + f'\n{data["xm"]}打卡成功')
            print('——————————————————')
            send_mail(data['email'], detail_time + '打卡成功', '今日打卡成功')
        else:
            now = datetime.datetime.now()
            now = now + datetime.timedelta(hours=0)
            detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
            # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
            # file_handle.writelines(detail_time + f'\n{data["xm"]}打卡失败\n')
            # file_handle.writelines('——————————————————\n')
            # file_handle.close()
            print(detail_time + f'\n{data["xm"]}打卡失败')
            print('——————————————————')
            send_mail(data.get('email'), detail_time + '打卡失败', '未知原因错误，请手动打卡')
    # except Exception as err:
    #     now = datetime.datetime.now()
    #     now = now + datetime.timedelta(hours=0)
    #     detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
    #     # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
    #     # file_handle.writelines(detail_time + f'\n{data["xm"]}打卡失败\n错误代码：{str(err)}\n')
    #     # file_handle.writelines('——————————————————\n')
    #     # file_handle.close()
    #     print(detail_time + f'\n{data["xm"]}打卡失败\n错误代码：{str(err)}')
    #     print('——————————————————')
        # send_mail(data.get("email"), detail_time + '打卡失败', '未知原因错误，请手动打卡\n错误代码：\n' + str(err))


# def main(event, context):
if __name__ == "__main__":
    now = datetime.datetime.now()
    now = now + datetime.timedelta(hours=0)
    detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
    # file_handle = open(LOG_FILE, mode='w', encoding='utf-8')
    # file_handle.writelines(detail_time + '\n开始运行\n')
    # file_handle.writelines('——————————————————\n')
    # file_handle.close()
    print(detail_time + '\n开始运行')
    print('——————————————————')
    mark = True
    # now = datetime.datetime.now()
    # now = now + datetime.timedelta(hours=0)

    # if now.strftime("%m-%d") > "07-15":
    #     detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
    #     # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
    #     # file_handle.writelines(detail_time + '\n假期停止运行\n')
    #     # file_handle.writelines('——————————————————\n')
    #     # file_handle.close()
    #     print(detail_time + '\n假期停止运行')
    #     print('——————————————————')
    #     exit()

    # if mark and now.strftime('%H') >= '18':
    # if mark or now.strftime('%H') >= '18':
    detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
    # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
    # file_handle.writelines(detail_time + '\n开始打卡\n')
    # file_handle.writelines('——————————————————\n')
    # file_handle.close()
    print(detail_time + '\n开始打卡')
    print('——————————————————')

    # sleep(random.randint(12, 180))
    if os.path.exists('userdata.json'):
        with open('userdata.json', 'r', encoding='utf-8') as f:
            item = json.loads(f.read())
            now = datetime.datetime.now()
            now = now + datetime.timedelta(hours=0)
            detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
            # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
            # file_handle.writelines(detail_time + f'\n开始为{item["xm"]}打卡\n')
            # file_handle.writelines('——————————————————\n')
            # file_handle.close()
            print(detail_time + f'\n开始为{item.get("xm")}打卡')
            print('——————————————————')
            daka(item)
            # sleep(random.randint(30, 60))

            now = datetime.datetime.now()
            now = now + datetime.timedelta(hours=0)
            detail_time = now.strftime('%Y-%m-%d %H:%M:%S')
            # file_handle = open(LOG_FILE, mode='a', encoding='utf-8')
            # file_handle.writelines(detail_time + '\n进入等待\n')
            # file_handle.writelines('——————————————————\n')
            # file_handle.close()
            print(detail_time + '\n进入等待')
            print('——————————————————')

import requests
import json
from email.mime.text import MIMEText
import smtplib
import time,datetime
from pyquery import PyQuery as pq

MSG_FROM = '' # 发送方邮箱
PASSWD = '' # 填入发送方邮箱的授权码

users = [
# 此处可填写多个用户
    ['your username','yur password','your email'],
]

def sendEmail(msg_to,title,content):
    if len(msg_to) == 0:
        return
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = MSG_FROM
    msg['To'] = msg_to
    while True:
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com",465)
            s.login(MSG_FROM, PASSWD)
            s.sendmail(MSG_FROM, msg_to, msg.as_string())
            s.quit()
            break
        except Exception as e:
            print(e)
            print('send failure')

def login(username,password):
    url = 'https://sso.hitsz.edu.cn:7002/cas/login?service=http%3A%2F%2Fxgsm.hitsz.edu.cn%2Fzhxy-xgzs%2Fcommon%2FcasLogin%3Fparams%3DL3hnX21vYmlsZS94c0hvbWU%3D'
    S = requests.session()
    response = S.get(url)
    doc = pq(response.text)
    form = doc('#fm1')
    jsessionid = form.attr('action').split('=')[1].split('?')[0]
    lt = form.find('[name=lt]').attr('value')
    data = {
        "username": username,
        "password": password,
        "lt": lt,
        "execution": "e1s1",
        "_eventId": "submit",
        "vc_username": "",
        "vc_password": "",
    }
    S.post(url,data=data)
    return S

def report(username,password):
    try:
        S=login(username,password)
        response = S.post('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xs/csh')
        id = json.loads(response.text)['module']
        data = {
            "id":id,
            "brzgtw":"36.2",
            "stzkm":"01",
            "dqszd":"01",
            "hwgj":"",
            "hwcs":"",
            "hwxxdz":"",
            "dqszdsheng":"440000",
            "dqszdshi":"440300",
            "dqszdqu":"440305",
            "gnxxdz":"哈尔滨工业大学（深圳）",
            "dqztm":"01",
            "dqztbz":"",
            "brfsgktt":"0",
            "brsfjy":"",
            "brjyyymc":"",
            "brzdjlm":"",
            "brzdjlbz":"",
            "qtbgsx":"",
            "sffwwhhb":"0",
            "sftjwhjhb":"0",
            "tcyhbwhrysfjc":"0",
            "sftzrychbwhhl":"0",
            "sfjdwhhbry":"0",
            "tcjtfs":"",
            "tchbcc":"",
            "tccx":"",
            "tczwh":"",
            "tcjcms":"",
            "gpsxx":"",
            "sfjcqthbwhry":"0",
            "sfjcqthbwhrybz":"",
            "tcjtfsbz":"",
        }
        data = {"info":json.dumps({"model":data})}
        # 提交填报信息
        S.post('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xs/saveYqxx',data=data)
        # 检查信息是否成功提交
        response = S.post('http://xgsm.hitsz.edu.cn/zhxy-xgzs/xg_mobile/xs/getYqxxList')
        return json.loads(response.text)['module']['data'][0]['id']==id
    except Exception as e:
        print(e)
        return False

for u in users:
    if not report(u[0],u[1]):
        sendEmail(u[2],u[0]+'提交失败','')
    else:
        sendEmail(u[2],u[0]+'提交成功','')

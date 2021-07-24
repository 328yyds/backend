# !/usr/local/bin/python
# -*- coding:utf-8 -*-
import http.client
import random
import urllib

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 用户名是登录用户中心->验证码短信->产品总览->APIID
account = "C79115995"
# 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
password = "2fdca307bc3cecc8c1d730c51c4d901e"


def send_sms(text, tel):
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': tel, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_code(tel):
    code = str(random.randint(100000, 999999))
    text = "您的验证码是：" + code + "。\n请不要把验证码泄露给其他人。"
    send_sms(text, tel)
    return code

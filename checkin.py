# -*- coding:utf-8 -*-
import requests as req
import json
import datetime
import re, os
from time import sleep
import baiduyun_captcha


class Tly(object):
    """docstring for ClassName"""

    def __init__(self):
        """初始化"""
        # server酱开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
        self.sever = os.environ["SERVE"]
        # 填写server酱sckey,不开启server酱则不用填
        self.sckey = os.environ["SCKEY"]
        # 'SCU89402Tf98b7f01ca3394*********************************'

        # tly账号对应邮件地址和密码
        email = os.environ["EMAIL"]
        passwd = os.environ["PASSWD"]

        # Baidu智能文字识别获取到的 API Key 和 Secret Key
        self.api_key = os.environ["APIKEY"]
        self.secret_key = os.environ["SECRETKEY"]

        self.Login_url = "https://{}/modules/_login.php"
        self.captcha_url = "https://{}/other/captcha.php"
        self.Login_data = {
            'email': email,
            'passwd': passwd,
            'remember_me': 'week'
        }
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3739.0 Safari/537.36 Edg/75.0.111.0"
        }
        self.session = req.session()

    def __del__(self):
        print('Project Wait 5s...')
        sleep(5)

    def get_cat(self, domain):
        """获取&识别验证码"""
        try:
            content = self.session.get(self.captcha_url.format(domain), headers=self.header).content
            captcha_code = baiduyun_captcha.captche_main(image_data=content, ak=self.api_key, sk=self.secret_key)
            print(captcha_code)
            code_url = 'https://' + domain + '/modules/_checkin.php?captcha=' + captcha_code
            # print(code_url)
            data = self.session.get(str(code_url), headers=self.header)
        except Exception as e:
            print('Project Error...')
            with open("Error.data", 'a+', encoding='utf-8') as f:
                f.write(str(datetime.datetime.now()) + ':' + str(e) + '\n')
        else:
            result = re.findall(r'<script>alert(.*);self.location=document.referrer;</script>', data.text)
            # 已签到的情况下result为空
            if result:
                if result[0].encode('utf8') == "('验证码错误!')":
                    print('%s' % (result[0]))
                    self.get_cat(domain)
                else:
                    with open('ok.jj', 'a+') as f:
                        f.write(str(datetime.datetime.now()) + ':' + str(result[0]) + '\n')
                    print('%s' % (result[0]))
                    if self.sever == "on":
                        req.get('https://sc.ftqq.com/' + self.sckey + '.send?text=' + re.sub("[()]", "", result[0]))
            else:
                print('已签到完成，请勿重复签到！')

    def login(self, domain='tly.com'):
        """登录tly.com"""
        try:
            html = self.session.post(self.Login_url.format(domain), data=self.Login_data, headers=self.header,
                                     timeout=30)
            html.encoding = html.apparent_encoding
            Login_data = json.loads(html.text)
            print(Login_data['msg'])
        except Exception as e:
            print('Login Error!')
            with open("Error.data", 'a+', encoding='utf-8') as f:
                f.write(str(datetime.datetime.now()) + '：' + str(e) + '\n')
        else:
            if Login_data['ok'] == '1':
                print('Login OK!')
                self.get_cat(domain)

    def run(self):
        while True:
            now_time = datetime.datetime.now()
            # if (now_time.hour) and (now_time.minute) and (now_time.second):
            # 设置登陆时间
            if (int(now_time.hour) == int(7)) and (int(now_time.minute) == int(5)):
                if now_time.hour and now_time.minute:
                    # 获取Baacloud最新地址
                    Code_url = req.get('http://api.cn3.me/url.php?id=3')
                    domain = Code_url.url.split('/')[-3]
                    print(domain)
                    self.login(domain)
                    sleep(60)
            sleep(1)
            # break


if __name__ == '__main__':
    login_domain = 'tly.com'
    bc = Tly()
    bc.login(domain=login_domain)

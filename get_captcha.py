#!/usr/bin/env python
# encoding: utf-8

# get_captcha.py
# Author     : jirui
# Date       : 2016/11/1


import hashlib
import requests
import json
import base64


ID = ''
KEY = ''
HOST = 'http://api.dama2.com:7766/app/'
TYPE = 42


def md5str(str):  # md5加密字符串
    m = hashlib.md5(str.encode(encoding="utf-8"))
    return m.hexdigest()


def md5(byte):  # md5加密byte
    return hashlib.md5(byte).hexdigest()


class DamatuApi():

    def __init__(self, username='test', password='test'):
        self.username = username
        self.password = password

    def get_sign(self, param=b''):
        return md5(bytes(KEY) + bytes(self.username) + param).encode('utf-8')[:8]

    def get_pwd(self):
        return md5str(KEY + md5str(md5str(self.username) + md5str(self.password)))

    def post(self, path, params={}):
        response = requests.post(HOST + path, data=params)
        return response.content

    # 查询余额 return 是正数为余额 如果为负数 则为错误码
    def get_balance(self):
        data = {'appID': ID,
                'user': self.username,
                'pwd': self.get_pwd(),
                'sign': self.get_sign()
                }
        res = self.post('d2Balance', data)
        jres = json.loads(res)
        if jres['ret'] == 0:
            return jres['balance']
        else:
            return jres['ret']

    # 上传验证码 参数filePath 验证码图片路径 如d:/1.jpg type是类型， return 是答案为成功 如果为负数 则为错误码
    def decode(self):
        filePath = '存放照片路径'
        f = open(filePath, 'rb')
        fdata = f.read()
        filedata = base64.b64encode(fdata)
        f.close()
        data = {'appID': ID,
                'user': self.username,
                'pwd': self.get_pwd(),
                'type': TYPE,
                'fileDataBase64': filedata,
                'sign': self.get_sign(fdata)
                }
        res = self.post('d2File', data)
        jres = json.loads(res)
        if jres['ret'] == 0:
            # 注意这个json里面有ret，id，result，cookie，根据自己的需要获取
            return (jres['result'])
        else:
            return jres['ret']

if __name__ == '__main__':
    # 调用类型实例：
    # 1.实例化类型 参数是打码兔用户账号和密码
    dmt = DamatuApi()

    print dmt.get_balance()  # 查询余额
    print dmt.decode()  # 上传打码


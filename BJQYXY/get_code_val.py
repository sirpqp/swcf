import requests

import base64

import json


def tuxiang1():
    url = 'http://122.14.246.7:9001/ocr/entbeijing'
    with open('./check_code.jpg', 'rb') as f:
        fileBase64 = base64.b64encode(f.read()).decode()

    body = {
        'fileBase64': fileBase64
    }

    headers = {
        'Content-Type': 'application/json;charser=UTF-8'
    }

    res = requests.post(url, json=body, headers=headers)

    return res.content.decode()

if __name__ == '__main__':
    tuxiang1()

import pymysql

# 打开数据库连接
import time

import redis

# 外网连接阿里云数据库
import requests


def getComapny():

    db1 = pymysql.connect(host="39.107.85.81", port=3306, user="root", password="ZmGyeX7gHroIxgt2cJ", database="business", charset="utf8")

    # 使用cursor()方法获取操作游标
    cursor1 = db1.cursor()

    r = redis.Redis(host='39.104.150.122', port=6379, db=3)

    # 使用execute方法执行SQL语句
    cursor1.execute("SELECT value FROM not_data LIMIT 2100000, 100000")
    #
    # 使用 fetchone() 方法获取一条数据
    data = cursor1.fetchall()

    for i in data:

        company = i[0]

        # 取出值来进行对应
        # url = 'http://172.16.100.181:8991/redisManager/getKey?ename=%s' % company
        # response = requests.get(url)
        # print(response.content.decode())
        # item["company_name"] = i
        # qccid = response.content.decode()
        # url = 'https://www.qichacha.com/firm_%s.html' % qccid
        # r.sadd('ent_administrative_license_info:detail_urls', url)
        r.lpush('company', company)
        print(company)

        # yield company, qccid
    # 关闭数据库连接
    db1.close()


if __name__ == '__main__':
    company = getComapny()
    print(company)

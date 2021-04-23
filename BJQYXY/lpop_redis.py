import pymysql

import redis

from BJQYXY import settings


def getRedis():
    r = redis.Redis(host='39.104.150.122', port=6379, db=1)

    company = r.lpop('company')

    con = pymysql.connect(
        host=settings.HOST, port=settings.PORT,
        user=settings.USER, password=settings.PASSWORD,
        database=settings.NAME, charset="utf8"
    )

    # 使用cursor()方法获取操作游标
    cursor = con.cursor()

    cursor.execute(("SELECT 1 from ent_business_license_info where name='%s'" % company.decode()))
    company_exist = cursor.fetchone()

    if not company_exist:
        print(company.decode())
        cursor.close()
        con.close()
        return company.decode()


if __name__ == '__main__':
    company = getRedis()
    print(company)

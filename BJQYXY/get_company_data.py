import json

import requests
import time, datetime


def GetCompanyDate(company):
    url = 'http://192.168.100.7:8991/esscomm/companyQuery/queryCompanyInfoByName?name=%s&currentPage=1&pageSize=10'

    res = requests.post(url).content.decode()
    data = json.loads(res)
    # print(data)
    try:
        companydate = str(data['list'][0]['approved_time'])[:10]
    except:
        companydate =None
    if companydate:

        # print(companydate)
        timeArray = time.localtime(int(companydate))

        company_date = time.strftime("%Y-%m-%d", timeArray)
        # print(company_date)
        return company_date
    else:
        return None


if __name__ == '__main__':

    GetCompanyDate('九次方大数据信息集团有限公司')
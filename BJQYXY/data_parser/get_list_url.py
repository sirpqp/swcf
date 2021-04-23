"""
用于判断该企业是否存在通往【变更信息，主要人员】列表页的链接
"""

import scrapy

import time
import re

from BJQYXY.data_parser.investor_information import investorinformation


def getlisturl(response):
    """
    :param response:企业主页的响应内容
    :return: 该项目的url链接
    """
    time.sleep(1)
    # 获取通往变更信息页面的url
    # url存在于包含变更信息的div里面
    if '您可能频繁重复请求' in response.text:
        print(response.meta['company'] + '主页因频繁访问中断')
        return scrapy.Request(
            url=response.url,
            callback=getlisturl,
            meta=response.meta
        )
    else:
        if response.meta['cate'] == '出资历史信息':
            div_info = response.xpath("//div[@id='tzrlistThree'][contains(string(),'出资历史信息')]")[0]
        elif response.meta['cate'] == '投资人信息':
            if response.xpath("//div[@id='tzrlistThree'][contains(string(), {0})]".format(response.meta['cate'])):
                div_info = response.xpath("//div[@id='tzrlistThree'][contains(string(), {0})]".format(response.meta['cate']))[0]
            elif response.xpath("//div[@id='tzrlistThree'][contains(string(),'主管部门（隶属单位）信息')]"):
                div_info = response.xpath("//div[@id='tzrlistThree'][contains(string(),'主管部门（隶属单位）信息')]")[0]
            else:
                div_info = ''
        else:
            div_info = response.xpath("//div[@id='zyrylistThree'][contains(string(), {0})]".format(response.meta['cate']))[0]
        if div_info:
            onclick_attr = div_info.xpath("./div[last()]/a[contains(text(),'更多')]/@onclick").extract_first()
            # 如果能在div里面找到onclick的属性值，则表示有该企业有变更信息
            if onclick_attr:
                list_page_url = re.compile(r"'(.*?)'", re.S).findall(onclick_attr)[0]
                listpageurl = 'http://qyxy.scjgj.beijing.gov.cn' + list_page_url
                if listpageurl:
                    return scrapy.Request(
                           url=listpageurl,
                           callback=investorinformation,
                           meta=response.meta
                        )
                else:
                    return None
                # return listpageurl
                # print(response.meta['company'] + '{0}url:'.format(cate) + listpageurl)
            # 否则表示该企业没有变更信息
        else:
            print(response.meta['company'], '{0}'.format(response.meta['cate']))


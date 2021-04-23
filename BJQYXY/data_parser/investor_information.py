"""
获取投资人信息
"""
import time
import re

from furl import furl

import scrapy

from BJQYXY.items import EntShareholderInvestmentInfoItem


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
            # 否则表示该企业没有变更信息
        else:
            print(response.meta['company'], '{0}'.format(response.meta['cate']))


def investorinformation(response):
    """
    解析投资人详情页
    :param response: 
    :return: 
    """
    if '您可能频繁重复请求' in response.text:
        print(response.meta['company'] + '列表页因频繁访问中断')
        yield scrapy.Request(
            url=response.url,
            callback=investorinformation,
            meta=response.meta
        )
    else:
        yield parse_detail(response)

        credit_ticket = re.compile(r'credit_ticket=(.*)', re.S).findall(response.url)[0]
        reg_bus_ent_id = re.compile('reg_bus_ent_id=(.*?)&', re.S).findall(response.url)[0]

        # 下一页
        try:
            pageNo = int(re.search(r"\d+", response.xpath("//a[@title='下一页']/@onclick").extract_first()).group())
        except Exception as e:
            print(34, "行  获取投资人信息", e)
            return ""

        # 总页
        pagescount = int(re.compile(r"共(\d+)页", re.S).findall(response.text)[0])

        # 是否进入下一页
        if pageNo < pagescount:
            page = 2 if pageNo == 1 else pageNo + 1
            params = {
                'reg_bus_ent_id': reg_bus_ent_id,
                'ent_page': '1',
                'moreInfo': '',
                'newInv': 'newInv',
                'fqr': '',
                'credit_ticket': credit_ticket,
                'SelectPageSize': '10',
                'EntryPageNo': '2',
                'pageNo': page,
                'pageSize': '10',
            }
            f_url = furl(url='http://qyxy.scjgj.beijing.gov.cn/xycx/queryCreditAction!tzrlist_all.dhtml')
            f_url.args = params
            yield scrapy.Request(
                url=f_url.url,
                callback=investorinformation,
                meta=response.meta
            )


def parse_detail(response):
    # 数据存在于table里面
    tr_list = response.xpath("//table[@id='tableIdStyle']//tr")
    item_tab = {}

    for tr in tr_list:
        # 股东及出资表的部分信息信息
        shareholderinvestmentinfoitem = EntShareholderInvestmentInfoItem()
        if len(tr.xpath(".//th")) > 0:
            th_list = tr.xpath(".//th")
            for i, th in enumerate(th_list):
                if th.xpath("./text()").extract_first().strip() == '投资人名称':
                    item_tab['name'] = i
                elif th.xpath("./text()").extract_first().strip() == '投资人类型':
                    item_tab['type'] = i
                elif th.xpath("./text()").extract_first().strip() == '证照类型':
                    item_tab['certificate_type'] = i
                elif th.xpath("./text()").extract_first().strip() == '证照号码':
                    item_tab['certificate_code'] = i
        else:
            td_list = tr.xpath("./td")
            for j, td in enumerate(td_list):
                if item_tab['name'] == j:
                    shareholderinvestmentinfoitem['name'] = td.xpath("./text()").extract_first().strip()
                elif item_tab['type'] == j:
                    shareholderinvestmentinfoitem['type'] = td.xpath("./text()").extract_first().strip()
                elif item_tab['certificate_type'] == j:
                    shareholderinvestmentinfoitem['certificate_type'] = td.xpath("./text()").extract_first().strip()
                elif item_tab['certificate_code'] == j:
                    shareholderinvestmentinfoitem['certificate_code'] = td.xpath("./text()").extract_first().strip()

            if shareholderinvestmentinfoitem:
                # 向投资人信息历史投资信息发送请求
                response.meta['shareholderinvestmentinfoitem'] = shareholderinvestmentinfoitem
                # print(response)
                req = getlisturl(response.meta['index_response'])
                if req:
                    yield req

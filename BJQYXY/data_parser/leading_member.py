import re
import datetime
import time

import scrapy
from furl import furl

from BJQYXY.items import EntMajorPersonInfoItem

from logging import getLogger

logger = getLogger('spider')


def majorpersoninfo(response):
    time.sleep(0.5)
    if '您可能频繁重复请求' in response.text:
        return scrapy.Request(
            url=response.url,
            callback=majorpersoninfo,
            meta=response.meta,
            dont_filter=False,
        )

    else:
        # 先判断是否存在主要人员信息的链接
        infor_div = ''
        if response.xpath("//div[@id='zyrylistThree'][contains(string(),'主要人员')]"):
            try:
                infor_div = response.xpath("//div[@id='zyrylistThree'][contains(string(),'主要人员')]")[0]
            except Exception as e:
                return
            onclick_attr = infor_div.xpath('./div[last()]/div/a/@onclick').extract_first()
            try:
                detail_url = re.compile(r"'(.*?)'", re.S).findall(onclick_attr)[0]
            except Exception as e:
                detail_url = ''
            if detail_url:
                detailurl = 'http://qyxy.scjgj.beijing.gov.cn' + detail_url
                return scrapy.Request(
                    url=detailurl,
                    callback=parse_detail,
                    meta=response.meta,
                )


def parse_detail(response):
    if '您可能频繁重复请求' in response.text:
        return scrapy.Request(
            url=response.url,
            callback=parse_detail,
            meta=response.meta,
            dont_filter=False,
        )
    else:

        # 下一页
        try:
            # 翻页所需要的2个参数
            credit_ticket = re.compile(r'credit_ticket=(.*)', re.S).findall(response.url)[0]
            reg_bus_ent_id = re.compile('reg_bus_ent_id=(.*?)&', re.S).findall(response.url)[0]
            next_page = int(re.search(r"\d+", response.xpath("//a[@title='下一页']/@onclick").extract_first()).group())
            # 总页数
            pagescount = int(re.compile(r"共(\d+)页", re.S).findall(response.text)[0])
            # 是否进入下一页
            if next_page < pagescount:
                # page = 2 if next_page == 1 else next_page + 1
                params = {
                    'reg_bus_ent_id': reg_bus_ent_id,
                    'ent_page': '1',
                    'moreInfo': '',
                    'newInv': 'newInv',
                    'fqr': '',
                    'credit_ticket': credit_ticket,
                    'SelectPageSize': '10',
                    'EntryPageNo': '2',
                    'pageNo': next_page,
                    'pageSize': '10',
                }
                f_url = furl(url='http://qyxy.scjgj.beijing.gov.cn/xycx/queryCreditAction!tzrlist_all.dhtml')
                f_url.args = params
                yield scrapy.Request(
                    url=f_url.url,
                    callback=parse_detail,
                    meta=response.meta
                )
        except Exception as e:
            # logger.error(response.meta['company']+'主要人员信息翻页错误', str(e))
            pass

        # 数据存在于table里面
        tr_list = response.xpath("//table[@id='tableIdStyle']//tr")
        item_tab = {}
        for tr in tr_list:
            item = EntMajorPersonInfoItem()
            if len(tr.xpath(".//th")) > 0:
                th_list = tr.xpath(".//th")
                for i, th in enumerate(th_list):
                    if th.xpath("./text()").extract_first().strip() == '姓名':
                        item_tab['name'] = i
                    elif th.xpath("./text()").extract_first().strip() == '职位':
                        item_tab['department'] = i
            else:
                if item_tab:
                    td_list = tr.xpath("./td")
                    for j, td in enumerate(td_list):
                        if item_tab['name'] == j:
                            item['name'] = td.xpath("./text()").extract_first().strip()
                        elif item_tab['department'] == j:
                            try:
                                item['department'] = td.xpath("./text()").extract_first().strip()
                            except:
                                item['department'] = None
                    if item:
                        item['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                        item['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                        item['data_status'] = 1
                        item['empty_ratio'] = 0
                        item['business_license_id'] = response.meta['company']
                        item['area_id'] = '北京'
                        yield item

"""
投资人及出资历史信息
"""

import datetime
import re, time
import scrapy

from furl import furl

from BJQYXY.items import EntShareholderInvestmentInfoItem
from BJQYXY.items import EntShareholderSubcribeInfoItem
from BJQYXY.items import EntShareholderPaidInfoItem


def tzrxinxi(response):
    """
    获取投资人信息
    :param response:
    :return:
    """
    if '您可能频繁重复请求' in response.text:
        time.sleep(3)
        return scrapy.Request(
            url=response.url,
            callback=tzrxinxi,
            meta=response.meta,
            dont_filter=True,
        )
    else:
        response.meta['index_response'] = response
        div_info = ''
        if response.xpath("//div[@id='tzrlistThree'][contains(string(), '投资人信息')]"):
            div_info = response.xpath("//div[@id='tzrlistThree'][contains(string(), '投资人信息')]")[0]
        elif response.xpath("//div[@id='tzrlistThree'][contains(string(),'主管部门（隶属单位）信息')]"):
            div_info = response.xpath("//div[@id='tzrlistThree'][contains(string(),'主管部门（隶属单位）信息')]")[0]
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


def investorinformation(response):
    """
    判断详情页是否响应正常，并获取总页数进行翻页
    :param response:
    :return:
    """
    if '您可能频繁重复请求' in response.text:
        yield scrapy.Request(
            url=response.url,
            callback=investorinformation,
            meta=response.meta,
            dont_filter=True,
        )
    else:
        # for shareholderinvestmentinfoitem in parse_czrxinxi_detail(response):
        item_list = parse_czrxinxi_detail(response)
        response.meta['item_list'] = item_list
        # response.meta['shareholderinvestmentinfoitem'] = shareholderinvestmentinfoitem
        # 获取通往历史出资人页面的链接
        czlsxinxi_url = czlsxinxi(response.meta['index_response'])
        # 拿到出资人信息后向历史投资信息发请求
        if czlsxinxi_url:
            yield scrapy.Request(
                url=czlsxinxi_url,
                callback=historicinvestmentinformation,
                meta=response.meta,
            )

        # 下一页
        try:
            # 翻页所需要的2个参数
            credit_ticket = re.compile(r'credit_ticket=(.*)', re.S).findall(response.url)[0]
            reg_bus_ent_id = re.compile('reg_bus_ent_id=(.*?)&', re.S).findall(response.url)[0]
            next_page = int(re.search(r"\d+", response.xpath("//a[@title='下一页']/@onclick").extract_first()).group())
            # 总页数
            pagescount = int(re.compile(r"共(\d+)页", re.S).findall(response.text)[0])
        except Exception as e:
            # 为了下面的if判断不报错，并且不往下执行代码，于是令next_page为一个大于总页数的数字
            next_page = 500
            pagescount = 100

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
                callback=investorinformation,
                meta=response.meta
            )


def parse_czrxinxi_detail(response):
    item_list = []
    # 数据存在于table里面
    tr_list = response.xpath("//table[@id='tableIdStyle']//tr")
    item_tab = {}
    for tr in tr_list:
        # 股东及出资信息表
        shareholderinvestmentinfoitem = EntShareholderInvestmentInfoItem()
        # 姓名
        shareholderinvestmentinfoitem['name'] = None
        # 股东类型
        shareholderinvestmentinfoitem['type'] = None
        # 证照/证件类型
        shareholderinvestmentinfoitem['certificate_type'] = None
        # 证照/证件号码
        shareholderinvestmentinfoitem['certificate_code'] = None
        # 认缴总额
        shareholderinvestmentinfoitem['subscribed_amount_sum'] = None
        # 认缴总额单位（万元）
        shareholderinvestmentinfoitem['subscribed_amount_sum_currency'] = None
        # 实缴总额
        shareholderinvestmentinfoitem['paid_amount_sum'] = None
        # 实缴总额单位（万元）
        shareholderinvestmentinfoitem['paid_amount_sum_currency'] = None
        # 创建日期
        shareholderinvestmentinfoitem['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        # 修改时间
        shareholderinvestmentinfoitem['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        # 所属区域
        shareholderinvestmentinfoitem['area_id'] = '北京'
        # 空置率
        shareholderinvestmentinfoitem['empty_ratio'] = 0
        # 数据当前状态
        shareholderinvestmentinfoitem['data_status'] = 1
        # 外键（营业执照）
        shareholderinvestmentinfoitem['business_license_id'] = response.meta['company']
        # 投资方式
        shareholderinvestmentinfoitem['investment_way'] = None
        # 公示日期
        shareholderinvestmentinfoitem['publish_date'] = None

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
            if td_list.__len__() > 2:
                for j, td in enumerate(td_list):
                    if item_tab['name'] == j:
                        # 投资人姓名
                        shareholderinvestmentinfoitem['name'] = td.xpath("./text()").extract_first().strip()
                    elif item_tab['type'] == j:
                        # 股东类型
                        shareholderinvestmentinfoitem['type'] = td.xpath("./text()").extract_first().strip()
                    elif item_tab['certificate_type'] == j:
                        # 证照/证件号码类型
                        shareholderinvestmentinfoitem['certificate_type'] = td.xpath("./text()").extract_first().strip()
                    elif item_tab['certificate_code'] == j:
                        # 证照/证件号码
                        shareholderinvestmentinfoitem['certificate_code'] = td.xpath("./text()").extract_first().strip()
                if shareholderinvestmentinfoitem:
                    # response.meta['shareholderinvestmentinfoitem'] = shareholderinvestmentinfoitem
                    item_list.append(shareholderinvestmentinfoitem)
    return item_list


def czlsxinxi(response):
    """
    获取历史出资信息
    :param response:
    :return:
    """
    div_info = ''
    try:
        div_info = response.xpath("//div[@id='tzrlistThree'][contains(string(),'出资历史信息')]")[0]
    except Exception as e:
        return None
    if div_info:
        onclick_attr = div_info.xpath("./div[last()]/a[contains(text(),'更多')]/@onclick").extract_first()
        # 如果能在div里面找到onclick的属性值，则表示有该企业有变更信息
        if onclick_attr:
            list_page_url = re.compile(r"'(.*?)'", re.S).findall(onclick_attr)[0]
            listpageurl = 'http://qyxy.scjgj.beijing.gov.cn' + list_page_url
            return listpageurl


def historicinvestmentinformation(response):
    """
    判断详情页是否响应正常，并解析详情页
    :param response:
    :return:
    """
    if '您可能频繁重复请求' in response.text:
        yield scrapy.Request(
            url=response.url,
            callback=historicinvestmentinformation,
            meta=response.meta,
            dont_filter=True,
        )
    else:
        # 解析详情页，得到认缴与实缴item
        item_list = parse_czlsxinxi_detail(response)
        for item in item_list:
            if len(item) == 3:
                shareholderinvestmentinfoitem = item[0]
                entshareholdesubcribeinfoitem = item[1]
                entshareholderpaidinfoitem = item[2]
                # 外键（股东及出资信息）
                entshareholdesubcribeinfoitem['shareholder_investment_id'] = response.meta['company'] + '+' + shareholderinvestmentinfoitem['name'] + '+' + shareholderinvestmentinfoitem['type']
                entshareholderpaidinfoitem['shareholder_investment_id'] = response.meta['company'] + '+' + shareholderinvestmentinfoitem['name'] + '+' + shareholderinvestmentinfoitem['type']
                yield shareholderinvestmentinfoitem

                # 实缴
                if entshareholdesubcribeinfoitem['subscribed_amount'] is not None and \
                   entshareholdesubcribeinfoitem['subscribed_amount_currency'] is not None:
                    yield entshareholdesubcribeinfoitem

                # 认缴
                if entshareholderpaidinfoitem['paid_amount'] is not None and \
                   entshareholderpaidinfoitem['paid_amount_currency'] is not None:
                    yield entshareholderpaidinfoitem


def parse_czlsxinxi_detail(response):
    item_list = []

    for shareholderinvestmentinfoitem in response.meta['item_list']:
        if shareholderinvestmentinfoitem['name'] in response.text:
            # 表示该投资人在出资历史页面有记录
            tr_list = response.xpath("//table[@id='tableIdStyle']//tr")
            # 用于存放表头所在列数的字典
            item_tab = {'name': '',
                        'type': '',
                        'subscribed_amount_sum': '',
                        'subscribed_type': '',
                        'subscribed_date': '',
                        'paid_amount_sum': '',
                        'paid_type': '',
                        'paid_date': '',
                        }
            for tr in tr_list:
                entshareholdesubcribeinfoitem = EntShareholderSubcribeInfoItem()
                # 认缴出资方式
                entshareholdesubcribeinfoitem['subscribed_type'] = None
                # 认缴总额
                entshareholdesubcribeinfoitem['subscribed_amount'] = None
                # 认缴出资额（万元）单位
                entshareholdesubcribeinfoitem['subscribed_amount_currency'] = None
                # 认缴出资日期
                entshareholdesubcribeinfoitem['subscribed_date'] = None
                # 创建日期
                entshareholdesubcribeinfoitem['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                # 修改时间
                entshareholdesubcribeinfoitem['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                # 所属区域
                entshareholdesubcribeinfoitem['area_id'] = '北京'
                # 空置率
                entshareholdesubcribeinfoitem['empty_ratio'] = 0
                # 数据当前状态
                entshareholdesubcribeinfoitem['data_status'] = 1
                # 外键（营业执照）
                entshareholdesubcribeinfoitem['business_license_id'] = response.meta['company']

                entshareholderpaidinfoitem = EntShareholderPaidInfoItem()
                # 实缴出资方式
                entshareholderpaidinfoitem['paid_type'] = None
                # 实缴总额
                entshareholderpaidinfoitem['paid_amount'] = None
                # 实缴出资额（万元）单位
                entshareholderpaidinfoitem['paid_amount_currency'] = None
                # 实缴出资日期
                entshareholderpaidinfoitem['paid_date'] = None
                # 创建日期
                entshareholderpaidinfoitem['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                # 修改时间
                entshareholderpaidinfoitem['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                # 所属区域
                entshareholderpaidinfoitem['area_id'] = '北京'
                # 空置率
                entshareholderpaidinfoitem['empty_ratio'] = 0
                # 数据当前状态
                entshareholderpaidinfoitem['data_status'] = 1
                # 外键（营业执照）
                entshareholderpaidinfoitem['business_license_id'] = response.meta['company']

                if len(tr.xpath(".//th")) > 0:
                    th_list = tr.xpath(".//th")
                    for i, th in enumerate(th_list):
                        if th.xpath("./text()").extract_first().strip() == '投资人名称':
                            item_tab['name'] = i
                        elif th.xpath("./text()").extract_first().strip() == '投资人类型':
                            item_tab['type'] = i
                        elif th.xpath("./text()").extract_first().strip() == '认缴出资金额':
                            # 认缴出资额（万元）单位
                            subscription = th.xpath("string(.)").extract_first().strip()
                            shareholderinvestmentinfoitem['subscribed_amount_sum_currency'] = re.search(r"（(.*?)）", subscription).group().replace("（", '').replace("）", '')
                            item_tab['subscribed_amount_sum'] = i
                        elif th.xpath("./text()").extract_first().strip() == '认缴出资方式':
                            item_tab['subscribed_type'] = i
                        elif th.xpath("./text()").extract_first().strip() == '认缴出资时间':
                            item_tab['subscribed_date'] = i
                        elif th.xpath("./text()").extract_first().strip() == '实缴出资金额':
                            # 实缴出资额（万元）单位
                            subscription = th.xpath("string(.)").extract_first().strip()
                            shareholderinvestmentinfoitem['paid_amount_sum_currency'] = re.search(r"（(.*?)）", subscription).group().replace("（", '').replace("）", '')
                            item_tab['paid_amount_sum'] = i
                        elif th.xpath("./text()").extract_first().strip() == '实缴出资方式':
                            item_tab['paid_type'] = i
                        elif th.xpath("./text()").extract_first().strip() == '实缴出资时间':
                            item_tab['paid_date'] = i
                else:
                    td_list = tr.xpath("./td")
                    if len(td_list) > 2:
                        name = td_list[1].xpath("./text()").extract_first().strip()
                        if shareholderinvestmentinfoitem['name'] == name:
                            for j, td in enumerate(td_list):
                                # 认缴出资方式
                                if item_tab['subscribed_type'] == j:
                                    entshareholdesubcribeinfoitem['subscribed_type'] = td.xpath("./text()").extract_first().strip()
                                # 认缴总额
                                elif item_tab['subscribed_amount_sum'] == j:
                                    entshareholdesubcribeinfoitem['subscribed_amount'] = td.xpath("./text()").extract_first().strip()
                                    shareholderinvestmentinfoitem['subscribed_amount_sum'] = td.xpath("./text()").extract_first().strip()
                                # 认缴出资日期
                                elif item_tab['subscribed_date'] == j:
                                    entshareholdesubcribeinfoitem['subscribed_date'] = td.xpath("./text()").extract_first().strip()
                                # 实缴出资方式
                                elif item_tab['paid_type'] == j:
                                    entshareholderpaidinfoitem['paid_type'] = td.xpath("./text()").extract_first().strip()
                                # 实缴总额
                                elif item_tab['paid_amount_sum'] == j:
                                    entshareholderpaidinfoitem['paid_amount'] = td.xpath("./text()").extract_first().strip()
                                    shareholderinvestmentinfoitem['paid_amount_sum'] = td.xpath("./text()").extract_first().strip()
                                # 实缴出资日期
                                elif item_tab['paid_date'] == j:
                                    entshareholderpaidinfoitem['paid_date'] = td.xpath("./text()").extract_first().strip()
                            entshareholdesubcribeinfoitem['subscribed_amount_currency'] = shareholderinvestmentinfoitem['subscribed_amount_sum_currency']
                            entshareholderpaidinfoitem['paid_amount_currency'] = shareholderinvestmentinfoitem['paid_amount_sum_currency']

                            item_list.append([shareholderinvestmentinfoitem, entshareholdesubcribeinfoitem, entshareholderpaidinfoitem])

        else:
            # 表示该投资人在出资历史页面没有记录
            entshareholdesubcribeinfoitem = EntShareholderSubcribeInfoItem()
            # 认缴出资方式
            entshareholdesubcribeinfoitem['subscribed_type'] = None
            # 认缴总额
            entshareholdesubcribeinfoitem['subscribed_amount'] = None
            # 认缴出资额（万元）单位
            entshareholdesubcribeinfoitem['subscribed_amount_currency'] = None
            # 认缴出资日期
            entshareholdesubcribeinfoitem['subscribed_date'] = None
            # 创建日期
            entshareholdesubcribeinfoitem['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 修改时间
            entshareholdesubcribeinfoitem['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 所属区域
            entshareholdesubcribeinfoitem['area_id'] = '北京'
            # 空置率
            entshareholdesubcribeinfoitem['empty_ratio'] = 0
            # 数据当前状态
            entshareholdesubcribeinfoitem['data_status'] = 1
            # 外键（营业执照）
            entshareholdesubcribeinfoitem['business_license_id'] = response.meta['company']

            entshareholderpaidinfoitem = EntShareholderPaidInfoItem()
            # 实缴出资方式
            entshareholderpaidinfoitem['paid_type'] = None
            # 实缴总额
            entshareholderpaidinfoitem['paid_amount'] = None
            # 实缴出资额（万元）单位
            entshareholderpaidinfoitem['paid_amount_currency'] = None
            # 实缴出资日期
            entshareholderpaidinfoitem['paid_date'] = None
            # 创建日期
            entshareholderpaidinfoitem['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 修改时间
            entshareholderpaidinfoitem['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 所属区域
            entshareholderpaidinfoitem['area_id'] = '北京'
            # 空置率
            entshareholderpaidinfoitem['empty_ratio'] = 0
            # 数据当前状态
            entshareholderpaidinfoitem['data_status'] = 1
            # 外键（营业执照）
            entshareholderpaidinfoitem['business_license_id'] = response.meta['company']

            item_list.append([shareholderinvestmentinfoitem, entshareholdesubcribeinfoitem, entshareholderpaidinfoitem])

    # 用于存放投资人信息页面的投资人名字
    tzrxinxi_name_list = []
    for shareholderinvestmentinfoitem in response.meta['item_list']:
        tzrxinxi_name_list.append(shareholderinvestmentinfoitem['name'])

    czlsxinxi_item_list = []
    # 数据存在于table里面
    tr_list = response.xpath("//table[@id='tableIdStyle']//tr")
    # 用于与存放表头所在列数的字典
    item_tab = {'name': '',
                'type': '',
                'subscribed_amount_sum': '',
                'subscribed_type': '',
                'subscribed_date': '',
                'paid_amount_sum': '',
                'paid_type': '',
                'paid_date': '',
                }
    for tr in tr_list:
        czlsxinxiitem = {}
        try:
            subscription = re.search(r"（(.*?)）", tr_list[0].xpath("string(.//th[4])").extract_first().strip()).group().replace("（", '').replace("）", '')
        except Exception as e:
            subscription = None
        czlsxinxiitem['subscribed_amount_sum_currency'] = subscription
        czlsxinxiitem['paid_amount_sum_currency'] = subscription
        if len(tr.xpath(".//th")) > 0:
            th_list = tr.xpath(".//th")
            for i, th in enumerate(th_list):
                if th.xpath("./text()").extract_first().strip() == '投资人名称':
                    item_tab['name'] = i
                elif th.xpath("./text()").extract_first().strip() == '投资人类型':
                    item_tab['type'] = i
                elif th.xpath("./text()").extract_first().strip() == '认缴出资金额':
                    # 认缴出资额（万元）单位
                    # subscription = th.xpath("string(.)").extract_first().strip()
                    # czlsxinxiitem['subscribed_amount_sum_currency'] = re.search(r"（(.*?)）", subscription).group().replace("（", '').replace("）", '')
                    item_tab['subscribed_amount_sum'] = i
                elif th.xpath("./text()").extract_first().strip() == '认缴出资方式':
                    item_tab['subscribed_type'] = i
                elif th.xpath("./text()").extract_first().strip() == '认缴出资时间':
                    item_tab['subscribed_date'] = i
                elif th.xpath("./text()").extract_first().strip() == '实缴出资金额':
                    # 实缴出资额（万元）单位
                    # subscription = th.xpath("string(.)").extract_first().strip()
                    # czlsxinxiitem['paid_amount_sum_currency'] = re.search(r"（(.*?)）", subscription).group().replace("（", '').replace("）", '')
                    item_tab['paid_amount_sum'] = i
                elif th.xpath("./text()").extract_first().strip() == '实缴出资方式':
                    item_tab['paid_type'] = i
                elif th.xpath("./text()").extract_first().strip() == '实缴出资时间':
                    item_tab['paid_date'] = i
        else:
            td_list = tr.xpath("./td")
            if len(td_list) > 2:
                for j, td in enumerate(td_list):
                    if item_tab['name'] == j:
                        czlsxinxiitem['name'] = td.xpath("./text()").extract_first().strip()
                    elif item_tab['type'] == j:
                        czlsxinxiitem['type'] = td.xpath("./text()").extract_first().strip()
                    # 认缴出资方式
                    elif item_tab['subscribed_type'] == j:
                        czlsxinxiitem['subscribed_type'] = td.xpath("./text()").extract_first().strip()
                    # 认缴总额
                    elif item_tab['subscribed_amount_sum'] == j:
                        czlsxinxiitem['subscribed_amount'] = td.xpath("./text()").extract_first().strip()
                    # 认缴出资日期
                    elif item_tab['subscribed_date'] == j:
                        czlsxinxiitem['subscribed_date'] = td.xpath("./text()").extract_first().strip()
                    # 实缴出资方式
                    elif item_tab['paid_type'] == j:
                        czlsxinxiitem['paid_type'] = td.xpath("./text()").extract_first().strip()
                    # 实缴总额
                    elif item_tab['paid_amount_sum'] == j:
                        czlsxinxiitem['paid_amount'] = td.xpath("./text()").extract_first().strip()
                    # 实缴出资日期
                    elif item_tab['paid_date'] == j:
                        czlsxinxiitem['paid_date'] = td.xpath("./text()").extract_first().strip()
                czlsxinxi_item_list.append(czlsxinxiitem)

    for czlsxinxi_item in czlsxinxi_item_list:
        # 如果投资历史页面中的的姓名不存在与投资人页面中，则需要补全股东及出资信息表
        if czlsxinxi_item['name'] not in tzrxinxi_name_list:
            shareholderinvestmentinfoitem_1 = EntShareholderInvestmentInfoItem()
            # 姓名
            shareholderinvestmentinfoitem_1['name'] = czlsxinxi_item['name']
            # 股东类型
            shareholderinvestmentinfoitem_1['type'] = czlsxinxi_item['type']
            # 证照/证件类型
            shareholderinvestmentinfoitem_1['certificate_type'] = None
            # 证照/证件号码
            shareholderinvestmentinfoitem_1['certificate_code'] = None
            # 认缴总额
            shareholderinvestmentinfoitem_1['subscribed_amount_sum'] = czlsxinxi_item['subscribed_amount']
            # 认缴总额单位（万元）
            shareholderinvestmentinfoitem_1['subscribed_amount_sum_currency'] = czlsxinxi_item['subscribed_amount_sum_currency']
            # 实缴总额
            shareholderinvestmentinfoitem_1['paid_amount_sum'] = czlsxinxi_item['paid_amount']
            # 实缴总额单位（万元）
            shareholderinvestmentinfoitem_1['paid_amount_sum_currency'] = czlsxinxi_item['paid_amount_sum_currency']
            # 创建日期
            shareholderinvestmentinfoitem_1['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 修改时间
            shareholderinvestmentinfoitem_1['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 所属区域
            shareholderinvestmentinfoitem_1['area_id'] = '北京'
            # 空置率
            shareholderinvestmentinfoitem_1['empty_ratio'] = 0
            # 数据当前状态
            shareholderinvestmentinfoitem_1['data_status'] = 1
            # 外键（营业执照）
            shareholderinvestmentinfoitem_1['business_license_id'] = response.meta['company']
            # 投资方式
            shareholderinvestmentinfoitem_1['investment_way'] = None
            # 公示日期
            shareholderinvestmentinfoitem_1['publish_date'] = None

            entshareholdesubcribeinfoitem_1 = EntShareholderSubcribeInfoItem()
            # 认缴出资方式
            entshareholdesubcribeinfoitem_1['subscribed_type'] = czlsxinxi_item['subscribed_type']
            # 认缴总额
            entshareholdesubcribeinfoitem_1['subscribed_amount'] = czlsxinxi_item['subscribed_amount']
            # 认缴出资额（万元）单位
            entshareholdesubcribeinfoitem_1['subscribed_amount_currency'] = czlsxinxi_item['subscribed_amount_sum_currency']
            # 认缴出资日期
            entshareholdesubcribeinfoitem_1['subscribed_date'] = czlsxinxi_item['subscribed_date']
            # 创建日期
            entshareholdesubcribeinfoitem_1['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 修改时间
            entshareholdesubcribeinfoitem_1['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 所属区域
            entshareholdesubcribeinfoitem_1['area_id'] = '北京'
            # 空置率
            entshareholdesubcribeinfoitem_1['empty_ratio'] = 0
            # 数据当前状态
            entshareholdesubcribeinfoitem_1['data_status'] = 1
            # 外键（营业执照）
            entshareholdesubcribeinfoitem_1['business_license_id'] = response.meta['company']

            entshareholderpaidinfoitem_1 = EntShareholderPaidInfoItem()
            # 实缴出资方式
            entshareholderpaidinfoitem_1['paid_type'] = czlsxinxi_item['paid_type']
            # 实缴总额
            entshareholderpaidinfoitem_1['paid_amount'] = czlsxinxi_item['paid_amount']
            # 实缴出资额（万元）单位
            entshareholderpaidinfoitem_1['paid_amount_currency'] = czlsxinxi_item['paid_amount_sum_currency']
            # 实缴出资日期
            entshareholderpaidinfoitem_1['paid_date'] = czlsxinxi_item['paid_date']
            # 创建日期
            entshareholderpaidinfoitem_1['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 修改时间
            entshareholderpaidinfoitem_1['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            # 所属区域
            entshareholderpaidinfoitem_1['area_id'] = '北京'
            # 空置率
            entshareholderpaidinfoitem_1['empty_ratio'] = 0
            # 数据当前状态
            entshareholderpaidinfoitem_1['data_status'] = 1
            # 外键（营业执照）
            entshareholderpaidinfoitem_1['business_license_id'] = response.meta['company']

            item_list.append([shareholderinvestmentinfoitem_1, entshareholdesubcribeinfoitem_1, entshareholderpaidinfoitem_1])

    return item_list


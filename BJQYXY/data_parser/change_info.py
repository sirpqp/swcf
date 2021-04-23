"""
变更信息
"""
import datetime
import re
import time
import json

from BJQYXY.items import *

tab_list = [
    '董事（理事）、经理、监事', '投资人',
    '实缴的出资额,实缴的出资方式,实缴的出资时间,实缴的出资方式,实缴的出资时间',
    '实缴的出资额,实缴的出资方式,实缴的出资方式', '认缴的出资额,认缴的出资方式,认缴的出资时间,实缴的出资额,实缴的出资方式,实缴的出资时间,投资人,认缴的出资方式,认缴的出资时间,实缴的出资额,实缴的出资方式,实缴的出资时间,投资人',
    '认缴的出资额,实缴的出资额,投资人,实缴的出资额,投资人'
]


def changeinformation(response):
    infor_div = response.xpath("//div[@class='cha-2'][contains(string(),'变更信息')]").xpath(
        './div[last()]/span/@onclick').extract_first()
    if infor_div:
        url = response.urljoin(re.compile(r"'(.*?)'", re.S).findall(infor_div)[0])
        return scrapy.Request(url, callback=get_list, meta=response.meta)


def get_list(response):
    # 详细页连接

    # tr_list = response.xpath("//table[@id='tableIdStyle']//tr//td/a/@onclick")
    result_list = response.xpath("//table[@id='tableIdStyle']//tr//td/a/@onclick/../../..")
    for tr in result_list:
        response.meta['change_date'] = tr.xpath("./td[2]/text()").extract_first().strip()
        response.meta['change_item'] = tr.xpath("./td[3]/text()").extract_first().strip()
        url = response.urljoin([i.strip() for i in re.split(r"'", tr.xpath("./td/a/@onclick").extract_first()) if i.strip() != ','][1])
        yield scrapy.Request(url, callback=get_detail, meta=response.meta)


def get_detail(response):
    if "您可能频繁重复请求" in response.text:
        time.sleep(0.5)
        yield scrapy.Request(response.url, callback=get_detail, dont_filter=True, meta=response.meta)
    elif len(response.xpath("//table[contains(string(),'变更')]")) == 0:
        time.sleep(0.5)
        yield scrapy.Request(response.url, callback=get_detail, dont_filter=True, meta=response.meta)
    else:
        item = EntChangeInfoItem()
        item['change_item'] = response.meta['change_item']
        item['change_date'] = response.meta['change_date']
        response.meta['item'] = item
        item_1 = parse_detail_page(response)
        if item_1:
            if type(item_1['befor_infor']) != str:
                item['change_before'] = json.dumps(item_1['befor_infor'], ensure_ascii=False)
                item['change_after'] = json.dumps(item_1['after_infor'], ensure_ascii=False)
            else:
                item['change_before'] = item_1['befor_infor']
                item['change_after'] = item_1['after_infor']
            if item:
                item['create_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                item['update_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                item['empty_ratio'] = 0
                item['area_id'] = '北京'
                item['data_status'] = 1
                item['business_license_id'] = response.meta['company']
                yield item


def parse_detail_page(response):
    item = {}
    """
    获取变更信息
    :param detail_res:详情页的响应对象
    :param item:每个变更项的item
    :return:每个变更项的item
    """
    # 如果变更项是属于上述列表中，说明变更前后是两个table
    if len(response.xpath("//table[contains(string(),'变更前')] | //table[contains(string(),'变更后')]")) == 2:
        table_1 = response.xpath("//table[@id='tableIdStyle'][contains(string(),'变更前')]")[0]
        item['befor_infor'] = get_change_infor(response.meta['item']['change_item'], table_1)

        table_2 = response.xpath("//table[@id='tableIdStyle'][contains(string(),'变更后')]")[0]
        item['after_infor'] = get_change_infor(response.meta['item']['change_item'], table_2)
    # 否则是一个table内包含变更前后的信息
    else:
        table = response.xpath("//table[@class='tableIdStyle'][contains(string(),'变更前')]")[0]
        change_infor = get_change_infor(response.meta['item']['change_item'], table)
        for i in change_infor:
            if i and (i['change_befor'] != None) and (i['change_befor'] != None):
                item['befor_infor'] = i['change_befor']
                item['after_infor'] = i['change_after']
    return item


def get_change_infor(change_item, table):
    """
    获取变更信息列表
    """
    if change_item in tab_list:
        tr_list = table.xpath(".//tr")[1:]
    elif change_item == '股东改变姓名或名称':
        tr_list = table.xpath("./tr")
    else:
        tr_list = table.xpath(".//tr")
    item_tab = {}
    change_infor = []
    for tr in tr_list:
        if tr.xpath(".//th").__len__() > 0:
            item_tab = get_item_tab(change_item, tr)
        else:
            # 获取每一行的变更信息，组成一个item，同时添加到变更信息列表中去
            if not item_tab:
                pass
            else:
                item = get_item(item_tab, tr)
                change_infor.append(item)
    return change_infor


def get_item_tab(change_item, tr):
    """
    获取表头所在列数
    :param change_item:变更项
    :param tr:表头所在的tr行
    :return: 表头所在列数
    """
    item_tab = {}
    th_list = tr.xpath(".//th")
    # 先给每个表头赋值，以免后续判断key值发生错误
    item_tab['name'] = ''
    item_tab['investor_type'] = ''
    item_tab['department'] = ''
    item_tab['investment_amount'] = ''
    item_tab['change_befor'] = ''
    item_tab['change_after'] = ''
    # 当变更类型在tab_list中时
    if (change_item in tab_list) or ('实缴的出资额' in change_item) or ('实缴的出资方式' in change_item) or ('认缴的出资额' in change_item):
        for i, th in enumerate(th_list):
            if th.xpath("./text()").extract_first().strip() == '姓名/名称':
                item_tab['name'] = i
            elif th.xpath("./text()").extract_first().strip() == '投资人类型':
                item_tab['investor_type'] = i
            elif th.xpath("./text()").extract_first().strip() == '姓名':
                item_tab['name'] = i
            elif th.xpath("./text()").extract_first().strip() == '职位':
                item_tab['department'] = i
            elif th.xpath("contains(text(), '出资金额')").extract_first() == '1':
                item_tab['investment_amount'] = i
    # 不在tab_list中时
    else:
        for i, th in enumerate(th_list):
            if th.xpath("./text()").extract_first().strip() == '变更前':
                item_tab['change_befor'] = i
            elif th.xpath("./text()").extract_first().strip() == '变更后':
                item_tab['change_after'] = i
    return item_tab


def get_item(item_tab, tr):
    """
    获取每一行的变更信息
    :param item_tab:表头所在列数
    :param tr:需要解析一行数据
    :return: 解析后的一行数据
    """
    item = {}
    # 如果tr中还包含table，需要单独解析
    if tr.xpath(".//table").__len__() > 0:
        change_infor = get_special_td(tr)
        return change_infor
    else:
        td_list = tr.xpath(".//td")
        for j, td in enumerate(td_list):
            # 投资人名称或董事（理事）、经理、监事名称
            if item_tab['name'] == j:
                name = td.xpath("./text()").extract_first().strip()
                if name:
                    item['name'] = name
                else:
                    item['name'] = None
            # 投资人类型
            elif item_tab['investor_type'] == j:
                investor_type = td.xpath("./text()").extract_first().strip()
                if investor_type:
                    item['investor_type'] = investor_type
                else:
                    item['investor_type'] = None
            # 职位
            elif item_tab['department'] == j:
                department = td.xpath("./text()").extract_first().strip()
                if department:
                    item['department'] = department
                else:
                    item['department'] = None
            # 出资金额
            elif item_tab['investment_amount'] == j:
                investment_amount = td.xpath("./text()").extract_first().strip()
                if investment_amount:
                    # investment_amount = investment_amount+'万元' if '万元' not in investment_amount else investment_amount
                    item['investment_amount'] = investment_amount+'万元' if '万元' not in investment_amount else investment_amount
                else:
                    item['investment_amount'] = None
            # 变更前
            elif item_tab['change_befor'] == j:
                change_befor = td.xpath("./text()").extract_first().strip().replace("\n", '').replace("\r", '').replace("\t", '')
                if change_befor:
                    item['change_befor'] = change_befor
                else:
                    item['change_befor'] = None
            # 变更后
            elif item_tab['change_after'] == j:
                change_after = td.xpath("./text()").extract_first().strip().replace("\n", '').replace("\r", '').replace("\t", '')
                if change_after:
                    item['change_after'] = change_after
                else:
                    item['change_after'] = None
    if item:
        return item


def get_special_td(tr):
    change_infor = {}
    table_list = tr.xpath(".//table")
    # 变更的信息
    # befor_text_list = table_list[0].xpath(".//td/text()")
    for ind, table_list in enumerate(table_list):
        infor = ''
        text_list = table_list.xpath(".//td/text()").extract()
        for i, text in enumerate(text_list):
            if text:
                infor += text.strip().replace("\n", '').replace("\r", '').replace("\t", '')
                if i != len(text_list) - 1:
                    infor += ','
        # 第一个table的内容是变更前的
        if ind == 0:
            change_infor['change_befor'] = infor
        # 第二个table的内容是变更前的
        elif ind == 1:
            change_infor['change_after'] = infor

    return change_infor

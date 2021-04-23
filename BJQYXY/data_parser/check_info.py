"""
提示信息 (抽查检查信息)
"""
import re
from furl import furl
from BJQYXY.items import *
from .business_license_Info import get_now_date


def get_check_url(response):
    data_count = response.xpath("//li[@id='TabbedPanelsTab_03']/span/text()").extract_first()
    if not data_count:
        return scrapy.Request(response.url, callback=get_check_url, meta=response.meta, dont_filter=True)
    # 判断是否有数据
    if int(data_count) > 0:
        # 构建url
        try:
            reg_bus_ent_id = response.xpath("//body/@onload").extract_first().split("','")[1]
        except:
            raise RuntimeError('entId没取到')
        params = {
            "reg_bus_ent_id": reg_bus_ent_id,
            "info_categ": '03',
            "vchr_bmdm": ""
        }
        f_url = furl("http://qyxy.scjgj.beijing.gov.cn/newChange/newChangeAction!getGj.dhtml")
        f_url.args = params
        response.meta['reg_bus_ent_id'] = reg_bus_ent_id
        return scrapy.Request(f_url.url, callback=checkinfo, meta=response.meta)


def checkinfo(response):
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=checkinfo, dont_filter=True, meta=response.meta)
    else:
        # 股权解冻信息
        unfreeze_tr_list = response.xpath("//td/a[contains(text(), '股权解冻信息')]/@onclick").extract_first()
        # 股权质押登记信息
        # pledge_tr_list = response.xpath("//td/a[contains(text(), '股权质押登记信息')]/@onclick").extract_first()
        # 抽查检查信息
        check_tr_list = response.xpath("//td/a[contains(text(), '抽查检查信息')]/@onclick").extract_first()
        # 年检验照信息
        annual_tr_list = response.xpath("//td/a[contains(text(), '年检验照信息')]/@onclick").extract_first()
        source = response.xpath('//tr/td[2]/text()').extract()
        # 数据来源
        # yield parse_list(response, tr_list)

        def parse_list(tr_list, table_type):
            """
            详细页解析方法
            """
            # 遍历所有的tr
            f_url = furl("http://qyxy.scjgj.beijing.gov.cn/newChange/newChangeAction!getCreditInfoInQyxx.dhtml")
            args = [i.strip() for i in re.split(r"'", tr_list) if i.strip() != ',']
            params = {
                "ent_id": response.meta['reg_bus_ent_id'],
                "info_categ": args[2],
                "chr_id": args[3].strip(","),
            }
            f_url.args = params
            response.meta['table_type'] = table_type
            response.meta["source"] = source
            return scrapy.Request(f_url.url, callback=parse_detial, meta=response.meta)

        # 详情数据解析
        # if unfreeze_tr_list:
        #     yield parse_list(unfreeze_tr_list, "股权解冻信息")
        # if pledge_tr_list:
        #     yield parse_list(pledge_tr_list, "股权质押登记信息")
        if check_tr_list:
            yield parse_list(check_tr_list, "抽查检查信息")
        # if annual_tr_list:
        #     yield parse_list(annual_tr_list, "年检验照信息")


def parse_detial(response):
    base_item = {
        "order_index": None,
        "create_date": get_now_date(),
        "update_date": None,
        "area_id": "北京",
        "empty_ratio": 0,
        "data_status": 1,
        "business_license_id": response.meta['company']
    }

    def get_text(response_table, text):
        try:
            content = response_table.xpath(".//td[@class='fen-6' and contains(text(),'" + text + "')]/following-sibling::td[1]/text()").extract_first().strip()
        except:
            try:
                content = response_table.xpath(".//td[@class='fen-6' and contains(text(),'" + text + "')]/following-sibling::td[1]/a/text()").extract_first().strip()
            except:
                content = None
        return content

    table_type = response.meta.get("table_type")
    # 多种数据解析分表
    for response_table in response.xpath("//table"):
        if table_type == "股权解冻信息":
            pass
            item = {
                "title": "股权解冻信息",
                "execute_court": get_text(response_table, "执行法院"),
                "execute_word_document": get_text(response_table, "执行文书文号"),
                "execute_matters": get_text(response_table, "执行事项"),
                "person_subject_to_enforcement": get_text(response_table, "被执行人"),
                "credentials_type": get_text(response_table, "被执行人证件种类"),
                "id_number": get_text(response_table, "被执行人证件号码"),
                "moeny": get_text(response_table, "被执行人持有股权"),
                "public_date": get_text(response_table, "公示日期"),
                "unfreeze_release_date": get_text(response_table, "解冻日期"),
                "unfreeze_authority": get_text(response_table, "解冻机关"),
                "unfreeze_word_document": get_text(response_table, "解冻文书号")}
        elif table_type == "股权质押登记信息":
            item = {"title": "股权质押登记信息",
                    "registration_number": get_text(response_table, "质权登记编号"),
                    "pledgor": get_text(response_table, "出质人"),
                    "pledgor_License_number": get_text(response_table, "出质人证照编号"),
                    "pledgee": get_text(response_table, "质权人"),
                    "pledgee_License_number": get_text(response_table, "质权人证照编号"),
                    "pledgor_equity_number": get_text(response_table, "出质股权数额"),
                    "pledgor_registration_date": get_text(response_table, "股权出质设立登记日期"),
                    "quality_status": get_text(response_table, "出质状态")}
        elif table_type == "抽查检查信息":
            item = EntCheckInfoItem()
            item["check_date"] = get_text(response_table, "抽查检查日期")
            item["check_organization"] = get_text(response_table, "检查实施机关")
            item["check_result"] = get_text(response_table, "抽查检查结果")
            item["check_type"] = get_text(response_table, "抽查检查类型")
        elif table_type == "年检验照信息":
            item = {
                "title": "年检验照信息",
                "check_year": response_table.xpath("//td[@class='fen-6' and contains(text(),'年检年度:')]/text()").extract_first().strip(),
                "check_year_result": response_table.xpath("//td[@class='fen-6' and contains(text(),'年检结果:')]/text()").extract_first().strip(),
                'source': response.meta["source"]
            }

        item.update(base_item)
        if list(item.values()).count(None) != 5:
            yield item

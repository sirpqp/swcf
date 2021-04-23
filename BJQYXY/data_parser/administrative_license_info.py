"""
行政许可信息
"""
import re
from BJQYXY.items import *
from furl import furl
from . business_license_Info import get_now_date


def licensin_qualification(response):
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=licensin_qualification, dont_filter=True, meta=response.meta)
    else:
        # 解析table表格内容
        tr_list = response.xpath("//td/a/@onclick").extract()
        for idx, td in enumerate(tr_list):
            args = [i.strip() for i in re.split(r"'", td) if i.strip() != ',']
            params = {
                "ent_id": response.meta['ent_id'],
                "info_categ": eval(re.split(',', td)[1]),
                "chr_id": args[3].strip(","),
            }
            f_url = furl("http://qyxy.scjgj.beijing.gov.cn/newChange/newChangeAction!getCreditInfoInQyxx.dhtml")
            f_url.args = params
            yield scrapy.Request(f_url.url, callback=parse_html, meta=response.meta)


def parse_html(response):
    # EntAdministrativeLicenseInfoItem
    item = {
        "order_index": None,
        "license_file_code": None,
        "license_file_name": None,
        "license_period_start": None,
        "license_period_end": None,
        "license_organization": None,
        "license_content": None,
        "create_date": get_now_date(),
        "update_date": None,
        "area_id": "北京",
        "empty_ratio": 0,
        "data_status": 1,
        "business_license_id": response.meta['company'],
    }

    def get_text(table, text):
        try:
            content = table.xpath(".//td[@class='fen-6' and contains(text(),'" + text + "')]/following-sibling::td[1]/text()").extract_first().strip()
        except:
            content = None
        return content

    for table in response.xpath("//table"):
        # 行政许可决定书文号
        item['license_file_code'] = get_text(table, "行政许可决定书文号")
        # 许可文件名称
        item["license_file_name"] = get_text(table, "项目名称")
        # 许可决定日期
        item['license_period_start'] = get_text(table, "许可决定日期")

        if item['license_period_start']:
            if item['license_period_start'] in ["长期", '— —', '-   -'] or len(item['license_period_start']) < 9:
                item['license_period_start'] = None
            elif "年" in item['license_period_start']:
                item['license_period_start'] = re.sub("年|月", "-", item['license_period_start'].strip("日"))
            if item['license_period_start']:
                item['license_period_start'] = item['license_period_start'][:10]
                start_index = item['license_period_start'].find(" ")
                if start_index != -1:
                    item['license_period_start'] = item['license_period_start'][:start_index]
                # print(item['license_period_start'])

        # 许可机关
        item['license_organization'] = get_text(table, "许可机关")
        # 许可内容
        item['license_content'] = get_text(table, "许可内容")

        if list(item.values()).count('— —') < 4:
            administrativelicenseinfo_Item = EntAdministrativeLicenseInfoItem()
            administrativelicenseinfo_Item.update(item)
            yield administrativelicenseinfo_Item

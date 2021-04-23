"""
企业警示信息
经营人异常信息
"""
import re
from BJQYXY.items import *
from .administrative_license_info import get_now_date


def companywarning(response):
    list_data = response.xpath("//div[@id='TabbedPanels1']//a")
    if list_data:
        # 获得chr_id参数
        chr_id = [i.strip() for i in re.split(r"'", list_data.xpath("./@onclick").extract_first()) if i.strip() != ','][
            3]
        # 拼接详情url
        detail_url = "http://qyxy.scjgj.beijing.gov.cn/newChange/newChangeAction!getCreditInfoInQyxx.dhtml?info_categ=040301&" + "chr_id=" + chr_id
        return scrapy.Request(detail_url, callback=get_item, meta=response.meta)


def get_item(response):
    """
    获得请求结果
    """

    def get_text(response_table, text):
        try:
            content = response_table.xpath(
                ".//td[@class='fen-6' and contains(text(),'" + text + "')]/following-sibling::td[1]/text()").extract_first().strip()
        except:
            try:
                content = response_table.xpath(
                    ".//td[@class='fen-6' and contains(text(),'" + text + "')]/following-sibling::td[1]/a/text()").extract_first().strip()
            except:
                content = None
        if content == '— —':
            return None
        return content

    item = {
        "order_index": None,
        "create_date": get_now_date(),
        "update_date": None,
        "area_id": "北京",
        "empty_ratio": 0,
        "data_status": 1,
        "business_license_id": response.meta['company']
    }
    for response_table in response.xpath("//table"):
        # 列入经营异常名录原因
        item["input_reason"] = get_text(response_table, "列入原因")
        # 列入日期
        item["input_date"] = get_text(response_table, "列入日期")
        # 作出决定机关(列入)
        item["input_organization"] = get_text(response_table, "作出决定机关(列入)")
        # 移出经营异常名录原因
        item["output_reason"] = get_text(response_table, "移出原因")
        # 移出日期
        item["output_date"] = get_text(response_table, "移出日期")
        # 作出决定机关（移出）
        item["output_organization"] = get_text(response_table, "作出决定机关（移出）")

        # 剔除不可用数据
        if item["input_reason"] is not None and \
                item["input_date"] is not None and \
                item["input_organization"] is not None:
            # 添加到对应的item种进行数据添加
            operationexceptioninfo_item = EntOperationExceptionInfoItem()
            operationexceptioninfo_item.update(item)
            yield operationexceptioninfo_item

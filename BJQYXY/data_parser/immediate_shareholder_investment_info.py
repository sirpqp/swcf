"""
股东及出资信息（企业即时信息）
"""
import re
from BJQYXY.items import *
from .business_license_Info import item


def companyShareholdersInvestment(response):
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=companyShareholdersInvestment, meta=response.meta, dont_filter=True)
    else:

        item['business_license_id'] = response.meta['company']
        if response.xpath("//td").__len__() == 0:
            return None

        # # 解析table表格内容
        tr_list = response.xpath('//*[@id="tableIdStyle" and contains(string(), "股东")]/tr')
        if tr_list:
            tr_list = tr_list[2:]
            for idx, tr in enumerate(tr_list):
                new_item = item

                shareholdersinvest_item = EntImmediateShareholderInvestmentInfo()
                # 股东
                try:
                    shareholdersinvest_item['name'] = tr.xpath("./td/text()").extract()[0].strip()
                    # 认缴额
                    shareholdersinvest_item['subscribed_amount_sum'] = tr.xpath("./td/text()").extract()[1].strip()
                    # 认缴单位
                    shareholdersinvest_item['subscribed_amount_sum_currency'] = "万元"
                    # 实缴额
                    shareholdersinvest_item['paid_amount_sum'] = tr.xpath("./td/text()").extract()[2].strip()
                    # 认缴单位
                    shareholdersinvest_item['paid_amount_sum_currency'] = "万元"
                    # 公示时间
                    shareholdersinvest_item['publish_time'] = None
                    # 公示日期
                    new_item['publish_date'] = None
                    shareholdersinvest_item.update(new_item)

                    yield shareholdersinvest_item
                except Exception as e:
                    print(e)

                immediateshareholdersubcribeinfo_item = EntImmediateShareholderSubcribeInfoItem()
                immediateshareholdersubcribeinfo_item['immediate_shareholder_investment_id'] = shareholdersinvest_item['name']

                # 认缴
                # 认缴出资方式
                immediateshareholdersubcribeinfo_item['subscribed_type'] = tr.xpath("./td/table//td/text()").extract()[
                    0].strip()
                # 认缴出资额
                immediateshareholdersubcribeinfo_item['subscribed_amount'] = \
                tr.xpath("./td/table//td/text()").extract()[1].strip()
                # 认缴出资额（万元）单位
                immediateshareholdersubcribeinfo_item["subscribed_amount_currency"] = "万元"
                # 认缴出资日期
                immediateshareholdersubcribeinfo_item['subscribed_date'] = re.sub("年|月", "-", tr.xpath(
                    "./td/table//td/text()").extract()[2].strip()).strip("日")
                immediateshareholdersubcribeinfo_item['publish_time'] = None

                # 判断是否是有用数据
                if (immediateshareholdersubcribeinfo_item['subscribed_type'] is not None) \
                        and (immediateshareholdersubcribeinfo_item['subscribed_date'] is not None) \
                        and (immediateshareholdersubcribeinfo_item['subscribed_amount'] is not None):
                    immediateshareholdersubcribeinfo_item.update(new_item)
                    yield immediateshareholdersubcribeinfo_item

                immediateshareholderpaidinfo_item = EntImmediateShareholderPaidInfoItem()
                immediateshareholderpaidinfo_item['immediate_shareholder_investment_id'] = shareholdersinvest_item[
                    'name']

                # 实缴
                # 实缴出资方式
                immediateshareholderpaidinfo_item['paid_type'] = tr.xpath("./td/table//td/text()").extract()[3].strip()
                # 实缴出资额
                immediateshareholderpaidinfo_item['paid_amount'] = tr.xpath("./td/table//td/text()").extract()[
                    4].strip()
                # 实缴出资额（万元）单位
                immediateshareholderpaidinfo_item["paid_amount_currency"] = "万元"
                # 实缴出资日期
                immediateshareholderpaidinfo_item['paid_date'] = re.sub("年|月", "-",
                                                                        tr.xpath("./td/table//td/text()").extract()[
                                                                            5].strip()).strip("日")
                # 判断是否是有用数据
                if (immediateshareholderpaidinfo_item['paid_type'] is not None) \
                        and (immediateshareholderpaidinfo_item['paid_date'] is not None) \
                        and (immediateshareholderpaidinfo_item['paid_amount'] is not None):
                    immediateshareholderpaidinfo_item.update(new_item)
                    yield immediateshareholderpaidinfo_item

        else:
            print('***无企业股东出资信息')

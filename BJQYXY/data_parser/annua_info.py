"""
企业年报
"""
import re

from furl import furl
from logging import getLogger
from .business_license_Info import get_now_date
from BJQYXY.items import *

logger = getLogger('spider')


def companyannual(response):
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=companyannual, meta=response.meta, dont_filter=True)
    else:
        annual_submission_link = response.xpath("//tr/td/a/@onclick").extract()
        # 年份
        annual_submission = response.xpath("//tr/td/a/text()").extract()

        # 发布日期
        date_publication = response.xpath("//tr/td[contains(text(),'-')]/text()").extract()

        # 详细信息
        for idx, value in enumerate(annual_submission):
            item = {}

            # 年报年份
            item['annua_name'] = value
            # 年报发布日期
            item['date_publication'] = date_publication[idx].strip()
            # 企业关联id
            item["company"] = response.meta['company']
            # 详细页信息

            detail_url = 'http://qyxy.scjgj.beijing.gov.cn' + re.search(r"(/.*?)'", annual_submission_link[idx]).group(1)
            yield scrapy.Request(detail_url, callback=companyannual_detail, meta=item)


def companyannual_detail(response):
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=companyannual, dont_filter=True, meta=response.meta)
    else:

        # # 企业年报基本信息
        annua_name = response.meta['annua_name']+response.meta['company']+"企业基本信息"
        yield get_basic_info(response)

        response.meta['annua_id'] = annua_name

        # 网站或网店信息
        wzFrame = response.xpath("//iframe[@id='wzFrame']/@src").extract_first()
        if wzFrame:
            url = "http://qyxy.scjgj.beijing.gov.cn" + wzFrame
            yield scrapy.Request(url, callback=get_website_info, meta=response.meta)

        # 股东及出资信息（企业年报信息）
        wzFrame = response.xpath("//iframe[@id='gdczFrame']/@src").extract_first()
        if wzFrame:
            url = "http://qyxy.scjgj.beijing.gov.cn" + wzFrame
            yield scrapy.Request(url, callback=get_annua_shareholder_investment_info, meta=response.meta)

        # 对外投资信息（企业年报信息）
        dwtzFrame = response.xpath("//iframe[@id='dwtzFrame']/@src").extract_first()
        if dwtzFrame:
            url = "http://qyxy.scjgj.beijing.gov.cn" + dwtzFrame
            yield scrapy.Request(url, callback=get_annua_out_investment_info, meta=response.meta)

        # 企业资产状况信息
        yield get_annua_property_asset_info(response)

        # 股权变更信息（企业年报信息）
        gdzrFrame = response.xpath("//iframe[@id='gdzrFrame']/@src").extract_first()
        if gdzrFrame:
            url = "http://qyxy.scjgj.beijing.gov.cn" + gdzrFrame
            yield scrapy.Request(url, callback=get_annua_equity_change_info, meta=response.meta)

        # 对外提供保证担保信息（企业年报信息）
        dwdbFrame = response.xpath("//iframe[@id='dwdbFrame']/@src").extract_first()
        if dwdbFrame:
            url = "http://qyxy.scjgj.beijing.gov.cn" + dwdbFrame
            yield scrapy.Request(url, callback=get_annua_out_guarantee_info, meta=response.meta)

        # 年报保险
        table = response.xpath("//table[@class='detailsList']//th[contains(.,'社保信息')]")
        if table:
            yield get_annua_social_security_Info(response)


def get_basic_info(response):
    """
    企业基本信息
    """

    def get_text(text):
        try:
            content = response.xpath("//th[contains(.,'" + text + "')]/following-sibling::td[1]/text()").extract_first()
        except:
            content = None
        return content

    entannuainfoitem = EntAnnuaInfoItem()
    item = {'operate_owner_phone': None, 'money_sum': 0, 'money_sum_currency': None, 'create_date': get_now_date(),
            'area_id': '北京', 'empty_ratio': 0, 'data_status': 1, 'affiliation': None, 'affiliation_code': None,
            'farmers_number': None, 'current_year_new_member': None, 'current_year_exit_member': None,
            'member_number': None,
            'women_number': None, 'main_business_scope': None, 'share_holding_status': None, 'update_date': None,
            'business_license_id': response.meta['company'],
            'annua_name': response.meta['annua_name'] + response.meta['company'] + "企业基本信息",
            'code_or_registration_no': get_text("注册号/统一社会信用代码"),
            'name': get_text("企业名称"), 'enterprise_phone': get_text("企业联系电话"), 'post_code': get_text("邮政编码"),
            'address': get_text("企业通信地址"), 'email': get_text("电子邮箱"),
            'own_share_change': get_text("有限责任公司本年度是否发生股东股权转让"), 'operate_status': get_text("企业经营状态"),
            'own_website': get_text("是否有网站或网店"), 'own_investment_or_merger': get_text("企业是否有投资信息或购买其他公司股权"),
            'employee_number': get_text("从业人数"), 'own_guarantee': get_text("是否有对外担保信息"), 'operate_owner': None}

    entannuainfoitem.update(item)
    return entannuainfoitem


def get_website_info(response):
    """
    网站或者网站信息
    """
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=get_website_info, meta=response.meta, dont_filter=True)
    else:
        tr_list = response.xpath("//table[@class='detailsList']//th[contains(.,'网站或网店信息')]/../..//td/..")
        item = {
            "order_index": None,
            "categary": None,
            "name": None,
            "url": None,
            "create_date": get_now_date(),
            "update_date": None,
            "empty_ratio": 0,
            "area_id": "北京",
            "data_status": 1,
            "business_license_id": response.meta['company'],
            "annua_id": response.meta['annua_id'],
        }
        for tr in tr_list:
            website_item = EntAnnuaWebsiteInfoItem()
            item['categary'] = tr.xpath("./td/text()")[0].extract().strip()
            item['name'] = tr.xpath("./td/text()")[1].extract().strip()
            item['url'] = tr.xpath("./td/text()")[2].extract().strip()
            website_item.update(item)
            yield website_item


def get_annua_shareholder_investment_info(response):
    """
    股东及出资信息（企业年报信息）
    EntAnnuaShareholderInvestmentInfoItem
    """
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=get_annua_shareholder_investment_info, meta=response.meta,
                             dont_filter=True)
    else:
        item = {
            "order_index": None,
            "name": None,
            "subscribed_amount_sum": None,
            "subscribed_amount_sum_currency": None,
            "subscribed_date": None,
            "subscribed_type": None,
            "paid_amount_sum": None,
            "paid_amount_sum_currency": None,
            "paid_date": None,
            "paid_type": None,
            "create_date": get_now_date(),
            "update_date": None,
            "empty_ratio": 0,
            "area_id": "北京",
            "data_status": 1,
            "business_license_id": response.meta['company'],
            "annua_id": response.meta['annua_id'],
        }
        tr_list = response.xpath("//table[@class='detailsList']//th[contains(.,'股东及出资信息 ')]/../..//td/..")
        for tr in tr_list:
            result_list = tr.xpath("./td/text()").extract()
            if len(result_list) != 7:
                result_list.insert(5, None)
            # 股东
            item['name'] = result_list[0]
            # 认缴出资额（万元）
            item['subscribed_amount_sum'] = result_list[1]
            item['subscribed_amount_sum_currency'] = result_list[1]
            # 认缴出资时间
            item['subscribed_date'] = result_list[2]
            # 认缴出资方式
            item['subscribed_type'] = result_list[3]
            # 实缴出资额
            item['paid_amount_sum'] = result_list[4]
            # 实缴出资额（万元）
            item['paid_amount_sum_currency'] = result_list[4]
            # 实缴出资时间
            item['paid_date'] = result_list[5]
            # 实缴出资方式
            item['paid_type'] = result_list[6]

            annuashareholderinvestment_item = EntAnnuaShareholderInvestmentInfoItem()
            annuashareholderinvestment_item.update(item)
            yield annuashareholderinvestment_item

            # 下一页
            pageNo = int(response.xpath("//input[@id='pageNo']/@value").extract_first())
            # 总页
            pagescount = int(response.xpath("//input[@id='pagescount']/@value").extract_first())

            # 是否进入下一页
            if pageNo < pagescount:
                page = 2 if pageNo == 1 else pageNo + 1
                params = {
                    'cid': str(response.xpath("//input[@name='cid']/@value").extract_first()),
                    "pageNo": page,
                    "pageSize": 5,
                }
                f_url = furl("http://qyxy.scjgj.beijing.gov.cn/entPub/entPubAction!gdcz_bj.dhtml")
                f_url.args = params
                yield scrapy.Request(f_url.url, callback=get_annua_shareholder_investment_info, meta=response.meta)


def get_annua_out_investment_info(response):
    """
    EntAnnuaOutInvestmentInfoItem
    对外投资信息（企业年报信息）
    """
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=get_annua_out_investment_info, meta=response.meta, dont_filter=True)
    else:
        item = {
            "enterprise_name": None,
            "registation_no": None,
            "create_date": get_now_date(),
            "update_date": None,
            "empty_ratio": 0,
            "area_id": "北京",
            "data_status": 1,
            "business_license_id": response.meta['company'],
            "annua_id": response.meta['annua_id'],
        }
        tr_list = response.xpath("//table[@class='detailsList']//th[contains(.,'对外投资信息 ')]/../..//td/..")
        for tr in tr_list:
            # 企业名
            item['enterprise_name'] = tr.xpath("./td/text()").extract()[0]
            # 注册号
            item['registation_no'] = tr.xpath("./td/text()").extract()[1]

            annuaoutinvestment_item = EntAnnuaOutInvestmentInfoItem()
            annuaoutinvestment_item.update(item)
            yield annuaoutinvestment_item

            # 下一页
            pageNo = int(response.xpath("//input[@id='pageNo']/@value").extract_first())
            # 总页
            pagescount = int(response.xpath("//input[@id='pagescount']/@value").extract_first())
            # 是否进入下一页
            if pageNo < pagescount:
                page = 2 if pageNo == 1 else pageNo + 1
                params = {
                    'cid': str(response.xpath("//input[@name='cid']/@value").extract_first()),
                    "pageNo": page,
                    "pageSize": 5,
                }
                f_url = furl("http://qyxy.scjgj.beijing.gov.cn/entPub/entPubAction!dwtz_bj.dhtml")
                f_url.args = params
                yield scrapy.Request(f_url.url, callback=get_annua_out_investment_info, meta=response.meta)


def get_annua_property_asset_info(response):
    """
    EntAnnuaPropertyAssetInfoItem
    企业资产状况信息（企业年报信息）
    """

    def get_text(text):
        try:
            content = response.xpath(
                "//th[contains(.,'" + text + "')]/following-sibling::td[1]/text()").extract_first().strip()
            if content == "企业选择不公示":
                content = None
        except:
            content = None
        return content

    annua_property_asset_item = EntAnnuaPropertyAssetInfoItem()

    property_asset_sum = get_text("资产总额")
    if property_asset_sum:
        property_asset_sum = property_asset_sum.strip("万元")
    item = {'property_asset_sum': property_asset_sum, 'own_power_sum': get_text("所有者权益合计"),
            'sales_sum': get_text("销售总额"),
            'profit_sum': get_text("利润总额"), 'operation_income_sum_main': get_text("营业总收入中主营业务收入"),
            'retained_profit': get_text("净利润"), 'tax_sum': get_text("纳税总额"), 'liability_sum': get_text("负债总额"),
            "operation_income_sum": None, "tax_sum": None, "currency": None, "create_date": get_now_date(),
            "update_date": None, "area_id": "北京",
            "empty_ratio": 0, "data_status": 1, "surplus_sum": None, "government_support_funds": None,
            "financial_credit": None, "property_asset_sum_currency": "万元",
            "own_power_sum_currency": None, "operation_income_sum_currency": None,
            "operation_income_sum_main_currency": None, "retained_profit_currency": None, "profit_sum_currency": None,
            "liability_sum_currency": None, "tax_sum_currency": None, "surplus_sum_currency": None,
            "government_support_funds_currency": None, "financial_credit_currency": None, "sales_sum_currency": None,
            "business_license_id": response.meta['company'], "annua_id": response.meta['annua_id']}
    if list(item.values()).count(None) < 20:
        annua_property_asset_item.update(item)
        return annua_property_asset_item


def get_annua_equity_change_info(response):
    """
    股权变更信息（企业年报信息）
    EntAnnuaEquityChangeInfoItem
    """
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=get_annua_equity_change_info, meta=response.meta, dont_filter=True)
    else:
        item = {
            "order_index": None,
            "name": None,
            "equity_change_before": None,
            "equity_change_after": None,
            "change_date": None,
            "create_date": get_now_date(),
            "update_date": None,
            "empty_ratio": 0,
            "area_id": "北京",
            "data_status": 1,
            "business_license_id": response.meta['company'],
            "annua_id": response.meta['annua_id'],
        }
        tr_list = response.xpath("//table[@class='detailsList']//th[contains(.,'股权变更信息 ')]/../..//td/..")
        for tr in tr_list:
            # 股东
            item['name'] = tr.xpath("./td/text()").extract()[0]
            # 变更前股权比例
            item['equity_change_before'] = tr.xpath("./td/text()").extract()[1]
            # 变更后股权比例
            item['equity_change_after'] = tr.xpath("./td/text()").extract()[2]
            # 股权变更日期
            item['change_date'] = tr.xpath("./td/text()").extract()[3]
            annuaoutinvestment_item = EntAnnuaEquityChangeInfoItem()
            annuaoutinvestment_item.update(item)
            yield annuaoutinvestment_item

            # 下一页
            pageNo = int(response.xpath("//input[@id='pageNo']/@value").extract_first())
            # 总页
            pagescount = int(response.xpath("//input[@id='pagescount']/@value").extract_first())
            # 是否进入下一页
            if pageNo < pagescount:
                page = 2 if pageNo == 1 else pageNo + 1
                params = {
                    'cid': str(response.xpath("//input[@name='cid']/@value").extract_first()),
                    "pageNo": page,
                    "pageSize": 5,
                }
                f_url = furl("http://qyxy.scjgj.beijing.gov.cn/entPub/entPubAction!gdzr_bj.dhtml")
                f_url.args = params
                yield scrapy.Request(f_url.url, callback=get_annua_equity_change_info, meta=response.meta)


def get_annua_out_guarantee_info(response):
    """
    EntAnnuaOutGuaranteeInfoItem
    对外提供保证担保信息（企业年报信息）
    """
    if "频繁重复请求" in response.text:
        yield scrapy.Request(response.url, callback=get_annua_out_guarantee_info, meta=response.meta, dont_filter=True)
    else:
        item = {
            "order_index": None,
            "creditor": None,
            "debtor": None,
            "creditor_right_categary": None,
            "creditor_right_sum": None,
            "creditor_right_sum_currency": "万元",
            "debtor_period": None,
            "guarantee_period": None,
            "guarantee_type": None,
            "create_date": get_now_date(),
            "update_date": None,
            "empty_ratio": 0,
            "area_id": "北京",
            "data_status": 1,
            "business_license_id": response.meta['company'],
            "annua_id": response.meta['annua_id'],
        }
        tr_list = response.xpath("//table[@class='detailsList']//th[contains(.,'对外提供保证担保信息')]/../..//td/..")
        for tr in tr_list:
            try:
                # 债权人
                item['creditor'] = tr.xpath("./td/text()").extract()[0]
                # 债务人
                item['debtor'] = tr.xpath("./td/text()").extract()[1]
                # 主债权种类
                item['creditor_right_categary'] = tr.xpath("./td/text()").extract()[2]
                # 主债权数额
                item['creditor_right_sum'] = tr.xpath("./td/text()").extract()[3].strip("万元")
                # # 履行债务的期限
                item['debtor_period'] = tr.xpath("./td/text()").extract()[4]
                # # 保证的期间
                item['guarantee_period'] = tr.xpath("./td/text()").extract()[5]
                # # 保证的方式
                item['guarantee_type'] = tr.xpath("./td/text()").extract()[6]
                # # 保证担保的范围
                # item['guarantee_scope'] = tr.xpath("./td/text()").extract()[7]
                annuaoutguaranteeinfo_item = EntAnnuaOutGuaranteeInfoItem()
                annuaoutguaranteeinfo_item.update(item)
                yield annuaoutguaranteeinfo_item
            except:
                logger.error(response.meta['company'] + "---" + "对外提供保证担保信息" + "---" + "抓取索引出现异常")

            # 下一页
            pageNo = int(response.xpath("//input[@id='pageNo']/@value").extract_first())
            # 总页
            pagescount = int(response.xpath("//input[@id='pagescount']/@value").extract_first())

            # 是否进入下一页
            if pageNo < pagescount:
                page = 2 if pageNo == 1 else pageNo + 1
                params = {
                    'cid': str(response.xpath("//input[@name='cid']/@value").extract_first()),
                    "pageNo": page,
                    "pageSize": 5,
                }
                f_url = furl("http://qyxy.scjgj.beijing.gov.cn/entPub/entPubAction!qydwdb_bj.dhtml")
                f_url.args = params
                yield scrapy.Request(f_url.url, callback=get_annua_out_guarantee_info, meta=response.meta)


# 股东变更信息（企业年报信息）
# 修改信息（企业年报信息）
# 行政许可信息（企业年报信息）

def get_annua_social_security_Info(response):
    """
    社保信息
    """

    def get_text(text):
        try:
            content = response.xpath("//th[contains(.,'" + text + "')]/following-sibling::td[1]/text()").extract()[
                0].strip()
        except:
            content = ""
        return content

    item = {
        'endowment_insurance': get_text("城镇职工基本养老保险"),
        'unemployment_insurance': get_text("失业保险"),
        'medical_insurance': get_text("职工基本医疗保险"),
        'employment_injury_insurance': get_text("工伤保险"),
        'maternity_insurance': get_text("生育保险"),
        "endowment_insurance_base": get_text("单位参加城镇职工基本养老保险缴费基数"),
        "unemployment_insurance_base": get_text("单位参加失业保险缴费基数"),
        "medical_insurance_base": get_text("单位参加职工基本医疗保险缴费基数"),
        "maternity_insurance_base": get_text("单位参加生育保险缴费基数"),
        "endowment_insurance_pay_amount": get_text("参加城镇职工基本养老保险本期实际缴费金额"),
        "unemployment_insurance_pay_amount": get_text("参加失业保险本期实际缴费金额"),
        "medical_insurance_pay_amount": get_text("参加职工基本医疗保险本期实际缴费金额"),
        "employment_injury_insurance_pay_amount": get_text("参加工伤保险本期实际缴费金额"),
        "maternity_insurance_pay_amount": get_text("参加生育保险本期实际缴费金额"),
        "endowment_insurance_owe_amount": get_text("单位参加城镇职工基本养老保险累计欠缴金额"),
        "unemployment_insurance_owe_amount": get_text("单位参加失业保险累计欠缴金额"),
        "medical_insurance_owe_amount": get_text("单位参加职工基本医疗保险累计欠缴金额"),
        "employment_injury_insurance_owe_amount": get_text("单位参加工伤保险累计欠缴金额"),
        "maternity_insurance_owe_amount": get_text("单位参加生育保险累计欠缴金额"),
        "create_date": get_now_date(),
        "update_date": None,
        'area_id': '北京',
        'empty_ratio': 0,
        'business_license_id': response.meta['company'],
        'annua_id': response.meta['annua_id'],
        'data_status': 1,
    }
    # print(item)

    annuasocialsecurity_item = EntAnnuaSocialSecurityInfoItem()
    annuasocialsecurity_item.update(item)
    return annuasocialsecurity_item

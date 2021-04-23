"""
营业执照信息
"""
from BJQYXY.items import QccItem


def get_now_date():
    import datetime
    return datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')


item = {
    "business_license_id": None,
    "create_date": get_now_date(),
    "update_date": None,
    "area_id": 0,
    "empty_ratio": 0,
    "data_status": 1,
}


def companybasic(response):
    business_license_item = {
        "code_or_registration_no": None,
        "name": None,
        "type": None,
        "legal_person": None,
        "money": None,
        "money_currency": None,
        "establish_date": None,
        "operating_period_start": None,
        "operating_period_end": None,
        "register_organization": None,
        "approval_date": None,
        "address": None,
        "register_status": None,
        "business_scope": None,
        "business_ower": None,
        "establish_form": None,
        "register_date": None,
        "create_date": None,
        "update_date": None,
        "area_id": None,
        "empty_ratio": None,
        "data_status": None,
        "logout_date": None,
        "revoke_date": None,
    }

    item = QccItem()
    try:
        td_list = response.xpath("//table[@class='f-lbiao'][1]//tr/td//text()")
        if td_list:
            for idx, i in enumerate(td_list):
                if i.extract() == '名称：':
                    try:
                        business_license_item['name'] = td_list[idx + 1].extract().strip()
                    except:
                        business_license_item['name'] = None

                if i.extract() == '统一社会信用代码：':
                    try:
                        business_license_item['code_or_registration_no'] = td_list[idx + 1].extract().strip()
                    except:
                        business_license_item['code_or_registration_no'] = None

                if i.extract() == '类型：':
                    try:
                        business_license_item['type'] = td_list[idx + 1].extract().strip()

                    except:
                        business_license_item['type'] = None

                if i.extract() == '法定代表人：':
                    try:
                        business_license_item['legal_person'] = td_list[idx + 1].extract().strip()
                    except:
                        business_license_item['legal_person'] = None

                if i.extract() == '住所：':
                    try:
                        business_license_item['address'] = td_list[idx + 1].extract().strip()
                    except:
                        business_license_item['address'] = None

                if i.extract() == '营业期限自：':
                    try:
                        business_license_item['operating_period_start'] = td_list[idx + 1].extract().strip()
                    except:
                        business_license_item['operating_period_start'] = None

                if i.extract() == '营业期限至：':
                    try:
                        business_license_item['operating_period_end'] = td_list[idx + 1].extract().strip()
                        if business_license_item['operating_period_end'] == "":
                            business_license_item['operating_period_end'] = None
                    except:
                        business_license_item['operating_period_end'] = None

                if i.extract() == '经营范围：':
                    try:
                        business_license_item['business_scope'] = td_list[idx + 1].extract().strip()

                    except:
                        business_license_item['business_scope'] = None

                if i.extract() == '登记机关：':
                    try:
                        business_license_item['register_organization'] = td_list[idx + 1].extract().strip()

                    except:
                        business_license_item['register_organization'] = None

                if i.extract() == '核准日期：':
                    try:
                        business_license_item['approval_date'] = td_list[idx + 1].extract().strip()

                    except:
                        business_license_item['approval_date'] = None

                if i.extract() == '成立日期：':
                    try:
                        business_license_item['establish_date'] = td_list[idx + 1].extract().strip()

                    except:
                        business_license_item['establish_date'] = None

                if i.extract() == '登记状态：':
                    try:
                        business_license_item['register_status'] = td_list[idx + 1].extract().strip()

                    except:
                        business_license_item['register_status'] = None

            td_list1 = response.xpath("//table[@class='f-lbiao'][2]//tr/td//text()")

            if td_list1:
                for idx, i in enumerate(td_list1):

                    if i.extract() == '注册资本：':
                        try:
                            business_license_item['money'], business_license_item['money_currency'] = td_list1[idx + 1].extract().strip().split(" ")
                        except:
                            business_license_item['money'] = None
                            business_license_item['money_currency'] = None

            # 所属区域
            business_license_item['area_id'] = "北京"
            # 数据当前状态
            business_license_item['data_status'] = 1
            # 创建时间
            business_license_item['create_date'] = get_now_date()
            # 修改时间
            business_license_item['update_date'] = None
            # 空置率
            business_license_item['empty_ratio'] = 0

    except Exception as e:
        print(e)
    item.update(business_license_item)
    return item


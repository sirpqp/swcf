# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QccItem(scrapy.Item):
    """
    营业执照信息
    """

    # 统一社会信用代码 / 注册号
    code_or_registration_no = scrapy.Field()

    # 企业名
    name = scrapy.Field()

    type = scrapy.Field()

    # 法人代表
    legal_person = scrapy.Field()

    # 注册资本
    money = scrapy.Field()

    # 注册资本币种
    money_currency = scrapy.Field()

    # 成立日期
    establish_date = scrapy.Field()

    # 营业期限自
    operating_period_start = scrapy.Field()

    # 营业期限至
    operating_period_end = scrapy.Field()

    # 登记机关
    register_organization = scrapy.Field()

    # 核准日期
    approval_date = scrapy.Field()

    # 住所
    address = scrapy.Field()

    # 登记状态
    register_status = scrapy.Field()

    # 经营范围
    business_scope = scrapy.Field()

    # 经营者
    business_ower = scrapy.Field()

    # 组成形式
    establish_form = scrapy.Field()

    # 注册日期
    register_date = scrapy.Field()

    # 创建时间
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 注销日期
    logout_date = scrapy.Field()

    # 吊销日期
    revoke_date = scrapy.Field()


class EntAdministrativeLicenseInfoItem(scrapy.Item):
    """
    行政许可
    """

    # 序号
    order_index = scrapy.Field()

    # 许可文件编号
    license_file_code = scrapy.Field()

    # 许可文件名称
    license_file_name = scrapy.Field()

    # 有效期自
    license_period_start = scrapy.Field()

    # 有效期至
    license_period_end = scrapy.Field()

    # 许可机关
    license_organization = scrapy.Field()

    # 许可内容
    license_content = scrapy.Field()

    # 创建时间
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntAdministrativePunishmentInfoItem(scrapy.Item):
    """
    行政处罚
    """

    # 序号
    order_index = scrapy.Field()

    # 决定书文号
    book_number = scrapy.Field()

    # 违法行为类型
    legal_type = scrapy.Field()

    # 决定机关名称
    punishment_organization = scrapy.Field()

    # 处罚决定日期
    punishment_date = scrapy.Field()

    # 公示日期
    publish_date = scrapy.Field()

    # 名称
    enterprise_name = scrapy.Field()

    # 统一社会信用代码/注册码
    registration_no = scrapy.Field()

    # 法定代表人（负责人）姓名
    legal_person = scrapy.Field()

    # 行政处罚内容
    punishment_content = scrapy.Field()

    # 判定书
    decision_book = scrapy.Field()

    # 创建时间
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntAnnuaInfoItem(scrapy.Item):
    """
    企业年报信息
    """

    # 企业年报信息
    annua_name = scrapy.Field()

    # 注册号 / 统一社会信用代码
    code_or_registration_no = scrapy.Field()

    # 企业名称
    name = scrapy.Field()

    # 企业联系电话
    enterprise_phone = scrapy.Field()

    # 邮政编码
    post_code = scrapy.Field()

    # 企业通信地址
    address = scrapy.Field()

    # 企业电子邮箱
    email = scrapy.Field()

    # 从业人数
    employee_number = scrapy.Field()

    # 企业经营状态
    operate_status = scrapy.Field()

    # 是否有网站或网店
    own_website = scrapy.Field()

    # 是否有投资信息或购买其他公司股权
    own_investment_or_merger = scrapy.Field()

    # 有限责任公司本年度是否发生股东股权转让
    own_share_change = scrapy.Field()

    # 是否有对外担保信息
    own_guarantee = scrapy.Field()

    # 经营者
    operate_owner = scrapy.Field()

    # 联系电话
    operate_owner_phone = scrapy.Field()

    # 资金数额
    money_sum = scrapy.Field()

    # 资金数额（单位）
    money_sum_currency = scrapy.Field()

    # 创建时间
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 隶属关系
    affiliation = scrapy.Field()

    # 隶属单位注册号
    affiliation_code = scrapy.Field()

    # 成员人数中农民人数
    farmers_number = scrapy.Field()

    # 本年度新增成员人数
    current_year_new_member = scrapy.Field()

    # 本年度退出成员人数
    current_year_exit_member = scrapy.Field()

    # 成员人数
    member_number = scrapy.Field()

    # 其中女性从业人数
    women_number = scrapy.Field()

    # 企业主营业务活动
    main_business_scope = scrapy.Field()

    # 企业控股情况
    share_holding_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntAnnuaOutInvestmentInfoItem(scrapy.Item):
    """
    对外投资信息（企业年报信息）
    """

    # 企业名称（对外投资）
    enterprise_name = scrapy.Field()

    # 企业注册号（对外投资）
    registation_no = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键（年报）
    annua_id = scrapy.Field()


class EntAnnuaPropertyAssetInfoItem(scrapy.Item):
    """
    企业资产状况信息（企业年报信息）
    """

    # 资产总额
    property_asset_sum = scrapy.Field()

    # 所有者权益合计
    own_power_sum = scrapy.Field()

    # 营业总收入
    operation_income_sum = scrapy.Field()

    # 营业总收入中主营业务收入
    operation_income_sum_main = scrapy.Field()

    # 净利润
    retained_profit = scrapy.Field()

    # 利润总额
    profit_sum = scrapy.Field()

    # 负债总额
    liability_sum = scrapy.Field()

    # 纳税总额
    tax_sum = scrapy.Field()

    # 单位
    currency = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 盈余总额
    surplus_sum = scrapy.Field()

    # 获得政府扶持资金, 补助
    government_support_funds = scrapy.Field()

    # 金融贷款
    financial_credit = scrapy.Field()

    # 销售总额
    sales_sum = scrapy.Field()

    # 资产总额单位
    property_asset_sum_currency = scrapy.Field()

    # 所有者权益合计单位
    own_power_sum_currency = scrapy.Field()

    # 营业总收入单位
    operation_income_sum_currency = scrapy.Field()

    # 营业总收入中主营业务收入单位
    operation_income_sum_main_currency = scrapy.Field()

    # 净利润单位
    retained_profit_currency = scrapy.Field()

    # 利润总额单位
    profit_sum_currency = scrapy.Field()

    # 负债总额单位
    liability_sum_currency = scrapy.Field()

    # 纳税总额单位
    tax_sum_currency = scrapy.Field()

    # 盈余总额单位
    surplus_sum_currency = scrapy.Field()

    # 获得政府扶持资金, 补助单位
    government_support_funds_currency = scrapy.Field()

    # 金融贷款单位
    financial_credit_currency = scrapy.Field()

    # 销售总额单位
    sales_sum_currency = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键（企业年报）
    annua_id = scrapy.Field()


class EntAnnuaShareholderInvestmentInfoItem(scrapy.Item):
    """
    股东及出资信息（企业年报信息）
    """

    # 序号
    order_index = scrapy.Field()

    # 股东
    name = scrapy.Field()

    # 认缴出资额
    subscribed_amount_sum = scrapy.Field()

    # 认缴出资额(单位万元)
    subscribed_amount_sum_currency = scrapy.Field()

    # 认缴出资时间
    subscribed_date = scrapy.Field()

    # 认缴出资方式
    subscribed_type = scrapy.Field()

    # 实缴出资额
    paid_amount_sum = scrapy.Field()

    # 实缴出资额(单位万元)
    paid_amount_sum_currency = scrapy.Field()

    # 实缴出资时间
    paid_date = scrapy.Field()

    # 实缴出资方式
    paid_type = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键（企业年报）
    annua_id = scrapy.Field()


class EntAnnuaWebsiteInfoItem(scrapy.Item):
    """
    网站或网店信息（企业年报信息）
    """

    # 序号
    order_index = scrapy.Field()

    # 类型
    categary = scrapy.Field()

    # 名称
    name = scrapy.Field()

    # 网址
    url = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键（企业年报）
    annua_id = scrapy.Field()


class EntAnnuaEquityChangeInfoItem(scrapy.Item):
    """
    股权变更信息（企业年报信息）
    """

    # 序号
    order_index = scrapy.Field()

    # 股东
    name = scrapy.Field()

    # 变更前股权比例
    equity_change_before = scrapy.Field()

    # 变更后股权比例
    equity_change_after = scrapy.Field()

    # 股权变更信息
    change_date = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键（企业年报）
    annua_id = scrapy.Field()


class EntAnnuaOutGuaranteeInfoItem(scrapy.Item):
    """
    对外提供保证担保信息（企业年报信息）
    """
    # 序号
    order_index = scrapy.Field()

    # 债权人
    creditor = scrapy.Field()

    # 债务人
    debtor = scrapy.Field()

    # 主债权种类
    creditor_right_categary = scrapy.Field()

    # 主债权数额
    creditor_right_sum = scrapy.Field()

    # 主债权数额（单位）
    creditor_right_sum_currency = scrapy.Field()

    # 履行债务的期限
    debtor_period = scrapy.Field()

    # 保证的期间
    guarantee_period = scrapy.Field()

    # 保证的方式
    guarantee_type = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键（企业年报）
    annua_id = scrapy.Field()


class EntBranchInfoItem(scrapy.Item):
    """
    分支机构信息
    """

    # 注册号
    registration_no = scrapy.Field()

    # 机构全称
    organization_name = scrapy.Field()

    # 机构责任人
    authority = scrapy.Field()

    # 创建时间
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntChangeInfoItem(scrapy.Item):
    """
    变更信息
    """

    # 变更事项
    change_item = scrapy.Field()

    # 变更前内容
    change_before = scrapy.Field()

    # 变更后内容
    change_after = scrapy.Field()

    # 变更日期
    change_date = scrapy.Field()

    # 创建时间
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntCheckInfoItem(scrapy.Item):
    """
    抽查检查信息
    """

    # 序号
    order_index = scrapy.Field()

    # 检查实施机关
    check_organization = scrapy.Field()

    # 类型
    check_type = scrapy.Field()

    # 日期
    check_date = scrapy.Field()

    # 结果
    check_result = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntEquityPledgedInfoItem(scrapy.Item):
    """
    股权出质信息
    """

    # 序号
    order_index = scrapy.Field()

    # 登记编号
    registration_no = scrapy.Field()

    # 出质人
    pledgor = scrapy.Field()

    # 证照 / 证件号码
    pledgor_certificate_no = scrapy.Field()

    # 出质股权数额
    equity_number = scrapy.Field()

    # 质权人
    pledgee = scrapy.Field()

    # 证照 / 证件号码
    pledgee_certificate_no = scrapy.Field()

    # 股权出质设立登记日期
    register_date = scrapy.Field()

    # 状态
    status = scrapy.Field()

    # 公示日期
    publish_time = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntEstateMortgageCancelInfoItem(scrapy.Item):
    """
    注销信息
    """

    # 注销日期
    cancel_date = scrapy.Field()

    # 注销原因
    cancel_reason = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license = scrapy.Field()

    # 外键（动产抵押登记信息）
    estate_mortgage = scrapy.Field()


class EntEstateMortgageInfoItem(scrapy.Item):
    """
    动产抵押登记信息
    """

    # 序号
    order_index = scrapy.Field()

    # 登记编号
    retister_code = scrapy.Field()

    # 登记日期
    retister_date = scrapy.Field()

    # 登记机关
    retister_organization = scrapy.Field()

    # 被担保债权数额
    guaranteed_number = scrapy.Field()

    # 被担保债权数额（万元）单位
    guaranteed_amount_currency = scrapy.Field()

    # 状态
    status = scrapy.Field()

    # 公示日期
    publish_date = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license = scrapy.Field()


class EntIllegalLostCreditInfoItem(scrapy.Item):
    """
    严重违法失信信息
    """

    # 序号
    order_index = scrapy.Field()

    # 列入严重违法失信企业原因
    input_reason = scrapy.Field()

    # 列入日期
    input_date = scrapy.Field()

    # 作出决定机关（列入）
    input_organization = scrapy.Field()

    # 移出严重违法失信企业原因
    output_reason = scrapy.Field()

    # 移出日期
    output_date = scrapy.Field()

    # 作出决定机关（移出）
    output_organization = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntLiquidationInfoItem(scrapy.Item):
    """
    清算信息
    """

    # 清算组负责人
    authority = scrapy.Field()

    # 清算组成员
    member = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntMajorPersonInfoItem(scrapy.Item):
    """
    主要人员
    """

    # 姓名
    name = scrapy.Field()

    # 职务
    department = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntOperationExceptionInfoItem(scrapy.Item):
    """
    经营异常信息
    """

    # 序号
    order_index = scrapy.Field()

    # 列入经营异常名录原因
    input_reason = scrapy.Field()

    # 列入日期
    input_date = scrapy.Field()

    # 作出决定机关（列入）
    input_organization = scrapy.Field()

    # 移出经营异常名录原因
    output_reason = scrapy.Field()

    # 移出日期
    output_date = scrapy.Field()

    # 作出决定机关（移出）
    output_organization = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()


class EntShareholderInvestmentInfoItem(scrapy.Item):
    """
    股东及出资信息
    """

    # 姓名-Y
    name = scrapy.Field()

    # 股东类型-Y
    type = scrapy.Field()

    # 证照/证件类型-Y
    certificate_type = scrapy.Field()

    # 证照/证件号码-Y
    certificate_code = scrapy.Field()

    # 认缴总额
    subscribed_amount_sum = scrapy.Field()

    # 认缴总额单位（万元）
    subscribed_amount_sum_currency = scrapy.Field()

    # 实缴总额
    paid_amount_sum = scrapy.Field()

    # 实缴总额单位（万元）
    paid_amount_sum_currency = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 投资方式
    investment_way = scrapy.Field()

    # 公示日期
    publish_date = scrapy.Field()


class EntShareholderSubcribeInfoItem(scrapy.Item):
    """
    认缴明细信息
    """

    # 认缴出资方式
    subscribed_type = scrapy.Field()

    # 认缴总额
    subscribed_amount = scrapy.Field()

    # 认缴出资额（万元）单位
    subscribed_amount_currency = scrapy.Field()

    # 认缴出资日期
    subscribed_date = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键（股东及出资信息）
    shareholder_investment_id = scrapy.Field()


class EntShareholderPaidInfoItem(scrapy.Item):
    """
    实缴明细消息
    """
    # 实缴出资方式
    paid_type = scrapy.Field()
    # 实缴总额
    paid_amount = scrapy.Field()
    # 实缴出资额（万元）单位
    paid_amount_currency = scrapy.Field()
    # 实缴出资日期
    paid_date = scrapy.Field()
    # 创建日期
    create_date = scrapy.Field()
    # 修改时间
    update_date = scrapy.Field()
    # 所属区域
    area_id = scrapy.Field()
    # 空置率
    empty_ratio = scrapy.Field()
    # 数据当前状态
    data_status = scrapy.Field()
    # 外键（营业执照）
    business_license_id = scrapy.Field()
    # 外键（股东及出资信息）
    shareholder_investment_id = scrapy.Field()


class EntImmediateShareholderInvestmentInfo(scrapy.Item):
    """
    股东及出资信息（企业即时信息）
    """
    # 姓名
    name = scrapy.Field()

    # 认缴总额
    subscribed_amount_sum = scrapy.Field()

    # 认缴总额单位（万元）
    subscribed_amount_sum_currency = scrapy.Field()

    # 实缴总额
    paid_amount_sum = scrapy.Field()

    # 实缴总额单位（万元）
    paid_amount_sum_currency = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 公示日期
    publish_date = scrapy.Field()

    # 公示日期
    publish_time = scrapy.Field()


class EntImmediateShareholderPaidInfoItem(scrapy.Item):
    """
    实缴明细（企业即时信息
    """
    # 实缴出资方式
    paid_type = scrapy.Field()

    # 实缴总额
    paid_amount = scrapy.Field()

    # 实缴出资额（万元）单位
    paid_amount_currency = scrapy.Field()

    # 实缴出资日期
    paid_date = scrapy.Field()

    # 公示时间
    publish_date = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键 股东及出资信息（企业即时信息）
    immediate_shareholder_investment_id = scrapy.Field()


class EntImmediateShareholderSubcribeInfoItem(scrapy.Item):
    """
    认缴明细（企业即时信息）
    """
    # 认缴出资方式
    subscribed_type = scrapy.Field()

    # 认缴总额
    subscribed_amount = scrapy.Field()

    # 认缴出资额（万元）单位
    subscribed_amount_currency = scrapy.Field()

    # 认缴出资日期
    subscribed_date = scrapy.Field()

    # 公示日期
    publish_time = scrapy.Field()

    # 公示时间
    publish_date = scrapy.Field()

    # 创建日期
    create_date = scrapy.Field()

    # 修改时间
    update_date = scrapy.Field()

    # 所属区域
    area_id = scrapy.Field()

    # 空置率
    empty_ratio = scrapy.Field()

    # 数据当前状态
    data_status = scrapy.Field()

    # 外键（营业执照）
    business_license_id = scrapy.Field()

    # 外键 股东及出资信息（企业即时信息）
    immediate_shareholder_investment_id = scrapy.Field()


class EntAnnuaSocialSecurityInfoItem(scrapy.Item):
    """
        社保信息（企业年报信息）
    """
    # 城镇职工基本养老保险
    endowment_insurance = scrapy.Field()
    # 失业保险
    unemployment_insurance = scrapy.Field()
    # 职工基本医疗保险
    medical_insurance = scrapy.Field()
    # 工伤保险
    employment_injury_insurance = scrapy.Field()
    # 生育保险
    maternity_insurance = scrapy.Field()
    # 单位参加城镇职工基本养老保险缴费基数
    endowment_insurance_base = scrapy.Field()
    # 单位参加失业保险缴费基数
    unemployment_insurance_base = scrapy.Field()
    # 单位参加职工基本医疗保险缴费基数
    medical_insurance_base = scrapy.Field()
    # 单位参加生育保险缴费基数
    maternity_insurance_base = scrapy.Field()
    # 参加城镇职工基本养老保险本期实际缴费金额
    endowment_insurance_pay_amount = scrapy.Field()
    # 参加失业保险本期实际缴费金额
    unemployment_insurance_pay_amount = scrapy.Field()
    # 参加职工基本医疗保险本期实际缴费金额
    medical_insurance_pay_amount = scrapy.Field()
    # 参加工伤保险本期实际缴费金额
    employment_injury_insurance_pay_amount = scrapy.Field()
    # 参加生育保险本期实际缴费金额
    maternity_insurance_pay_amount = scrapy.Field()
    # 单位参加城镇职工基本养老保险累计欠缴金额
    endowment_insurance_owe_amount = scrapy.Field()
    # 单位参加失业保险累计欠缴金额
    unemployment_insurance_owe_amount = scrapy.Field()
    # 单位参加职工基本医疗保险累计欠缴金额
    medical_insurance_owe_amount = scrapy.Field()
    # 单位参加工伤保险累计欠缴金额'
    employment_injury_insurance_owe_amount = scrapy.Field()
    # 单位参加生育保险累计欠缴金额
    maternity_insurance_owe_amount = scrapy.Field()
    # 创建时间
    create_date = scrapy.Field()
    # 修改时间
    update_date = scrapy.Field()
    # 所属区域
    area_id = scrapy.Field()
    # 空置率
    empty_ratio = scrapy.Field()
    # 外键（营业执照）
    business_license_id = scrapy.Field()
    # 外键 年报
    annua_id = scrapy.Field()
    # 当前状态
    data_status = scrapy.Field()

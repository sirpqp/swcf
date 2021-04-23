# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql
from .settings import NAME, PORT, USER, PASSWORD, HOST

from .items import *


class BjqyxyPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):

    # 打开数据库
    def open_spider(self, spider):
        # 连接数据库
        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER,
                                    password=PASSWORD, database=NAME, charset="utf8",
                                    cursorclass=pymysql.cursors.DictCursor, connect_timeout=10)
        # 建立游标
        self.cursors = self.conn.cursor()

    # 操作
    def process_item(self, item, spider):
        if item.get("empty_ratio") == "北京":
            item['empty_ratio'] = 0
            print(type(item), "*" * 10)

        try:
            # 操作值
            for val in item._values:
                if item.get(val) and isinstance(item.get(val), str):
                    item[val] = item.get(val).strip()
                if item.get(val) == "":
                    item[val] = None
        except:
            print(type(item))

        # 处理小数点
        if item.get("paid_amount_sum"):
            item['paid_amount_sum'] = "%.4f" % float(item['paid_amount_sum'])
        if item.get("paid_amount"):
            item['paid_amount'] = "%.4f" % float(item['paid_amount'])
        if item.get("subscribed_amount_sum"):
            item['subscribed_amount_sum'] = "%.4f" % float(item['subscribed_amount_sum'])
        if item.get("subscribed_amount"):
            item["subscribed_amount"] = "%.4f" % float(item["subscribed_amount"])
        if item.get("money"):
            item["money"] = "%.4f" % float(item["money"])
        if item.get("property_asset_sum"):
            item["property_asset_sum"] = "%.4f" % float(item["property_asset_sum"])

        # 操作外键

        # 营业执照信息
        if 'business_license_id' in item and not str(item['business_license_id']).isdigit():
            sql = "SELECT id from ent_business_license_info WHERE name = %s"

            self.conn.ping(reconnect=True)
            self.cursors.execute(sql, [item['business_license_id']])
            result = self.cursors.fetchone()
            if result:
                foreign_id = result.get('id', 0)
                if foreign_id != 0:
                    item['business_license_id'] = foreign_id
                else:
                    print("*" * 100)
            else:
                print(item['business_license_id'], "主表还没存")
                return None


        # 年报
        if 'annua_id' in item:
            sql = "SELECT id from ent_annua_info WHERE annua_name = %s"
            self.conn.ping(reconnect=True)
            self.cursors.execute(sql, [item['annua_id']])
            result = self.cursors.fetchone()
            if result:
                foreign_id = result.get('id', 0)
                if foreign_id != 0:
                    item['annua_id'] = foreign_id
                else:
                    print("-" * 100)
            else:
                return None
                print(item['business_license_id'], "主表还")

        # 企业即时信息
        if item.get('immediate_shareholder_investment_id'):
            sql = "SELECT id from ent_immediate_shareholder_investment_info WHERE name = %s"
            self.conn.ping(reconnect=True)
            self.cursors.execute(sql, [item['immediate_shareholder_investment_id']])
            result = self.cursors.fetchone()
            foreign_id = result.get('id', 0)
            if foreign_id != 0:
                item['immediate_shareholder_investment_id'] = foreign_id
            else:
                print("-" * 100)

        # 时间操作
        try:
            if item['subscribed_date']:
                item['subscribed_date'] = item['subscribed_date'][:10]

            if item['paid_date']:
                item['paid_date'] = item['paid_date'][:10]
        except:
            pass

        # 变更时间修改
        # if item.get("change_date", None):
        #     item['change_date'] = item['change_date'][:10]

        if item.get('shareholder_investment_id', None):
            li = item.get('shareholder_investment_id', None).split("+")
            sql = "select id from ent_shareholder_investment_info where name=%s and type =%s and business_license_id=%s"
            self.conn.ping(reconnect=True)
            self.cursors.execute(sql, [li[1], li[2], item['business_license_id']])
            result = self.cursors.fetchone()
            item['shareholder_investment_id'] = result['id']

        if isinstance(item, QccItem):
            try:
                # 插入数据
                sql = "insert into ent_business_license_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["code_or_registration_no"], item["name"], item["type"],

                                           item["legal_person"], item["money"], item["money_currency"],

                                           item["establish_date"], item["operating_period_start"],

                                           item["operating_period_end"], item["register_organization"],
                                           item["approval_date"],

                                           item["address"], item["register_status"], item["business_scope"],

                                           item["business_ower"], item["establish_form"],

                                           item["register_date"], item["create_date"], item["update_date"],
                                           item["area_id"],

                                           item["empty_ratio"], item["data_status"], item["logout_date"],
                                           item["revoke_date"]])
                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 行政许可
        elif isinstance(item, EntAdministrativeLicenseInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_administrative_license_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql,
                                     [0, item["order_index"], item["license_file_code"],
                                      item["license_file_name"],

                                      item["license_period_start"], item["license_period_end"],
                                      item["license_organization"],

                                      item["license_content"], item["create_date"],

                                      item["update_date"], item["area_id"],
                                      item["empty_ratio"],

                                      item["data_status"], item['business_license_id']])
                self.conn.commit()
            except Exception as e:
                print(e, type(item), item)

        # 行政处罚
        elif isinstance(item, EntAdministrativePunishmentInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_administrative_punishment_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"], item["book_number"],
                                           item["legal_type"],

                                           item["punishment_organization"], item["punishment_date"],
                                           item["publish_date"],

                                           item["enterprise_name"], item["registration_no"],

                                           item["legal_person"], item["punishment_content"],
                                           item["decision_book"], item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"],
                                           item["data_status"], item['business_license_id'], ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 企业年报信息
        elif isinstance(item, EntAnnuaInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_annua_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["annua_name"],
                                           item["code_or_registration_no"], item["name"],

                                           item["enterprise_phone"], item["post_code"], item["address"],

                                           item["email"], item["employee_number"],

                                           item["operate_status"], item["own_website"],
                                           item["own_investment_or_merger"], item["own_share_change"],
                                           item["own_guarantee"], item["operate_owner"],
                                           item["operate_owner_phone"], item["money_sum"],
                                           item["money_sum_currency"], item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["affiliation"], item["affiliation_code"], item["farmers_number"],
                                           item["current_year_new_member"], item["current_year_exit_member"],
                                           item["member_number"], item["women_number"],
                                           item["main_business_scope"], item["share_holding_status"],
                                           item['business_license_id'],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 对外投资信息（企业年报信息）
        elif isinstance(item, EntAnnuaOutInvestmentInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_annua_out_investment_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["enterprise_name"],
                                           item["registation_no"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"], item["annua_id"],
                                           item['business_license_id'],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 股权变更信息（企业年报信息）
        elif isinstance(item, EntAnnuaEquityChangeInfoItem):
            try:
                sql = "insert into ent_annua_equity_change_info values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                if item.get('change_date', None):
                    item["change_date"] = item['change_date'][:10]
                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [
                    0,
                    item["order_index"],
                    item["name"],
                    item["equity_change_before"],
                    item["equity_change_after"],
                    item["change_date"],
                    item["create_date"],
                    item["update_date"],
                    item["area_id"],
                    item["empty_ratio"],
                    item["data_status"],
                    item["annua_id"],
                    item["business_license_id"],
                ])
                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 企业资产状况信息（企业年报信息）
        elif isinstance(item, EntAnnuaPropertyAssetInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_annua_property_asset_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                if item["own_power_sum"]:
                    item["own_power_sum"] = '%.4f' % float(item["own_power_sum"].strip("万元"))
                if item['sales_sum']:
                    item["sales_sum"] = '%.4f' % float(item["sales_sum"].strip("万元"))
                if item['operation_income_sum_main']:
                    item["operation_income_sum_main"] = '%.4f' % float(item["operation_income_sum_main"].strip("万元"))
                if item['retained_profit']:
                    item["retained_profit"] = '%.4f' % float(item["retained_profit"].strip("万元"))
                if item['liability_sum']:
                    item["liability_sum"] = '%.4f' % float(item["liability_sum"].strip("万元"))
                if item['profit_sum']:
                    item['profit_sum'] = '%.4f' % float(item['profit_sum'].strip("万元"))
                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["property_asset_sum"],
                                           item["own_power_sum"],

                                           item["operation_income_sum"], item["operation_income_sum_main"],
                                           item["retained_profit"],

                                           item["profit_sum"], item["liability_sum"],

                                           item["tax_sum"], item["currency"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["surplus_sum"], item["government_support_funds"],
                                           item["financial_credit"],
                                           item["sales_sum"], item["property_asset_sum_currency"],
                                           item["own_power_sum_currency"], item["operation_income_sum_currency"],
                                           item["operation_income_sum_main_currency"], item["retained_profit_currency"],
                                           item["profit_sum_currency"], item["liability_sum_currency"],
                                           item["tax_sum_currency"], item["surplus_sum_currency"],
                                           item["government_support_funds_currency"], item["financial_credit_currency"],
                                           item["sales_sum_currency"], item["annua_id"], item['business_license_id'],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        elif isinstance(item, EntShareholderInvestmentInfoItem):
            # 股东及出资信息
            try:
                # 插入数据
                sql = "insert into ent_shareholder_investment_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0,
                                           item["name"], item["type"],

                                           item["certificate_type"], item["certificate_code"],
                                           item["subscribed_amount_sum"], item["subscribed_amount_sum_currency"],

                                           item["paid_amount_sum"], item["paid_amount_sum_currency"],
                                           item["create_date"], item["update_date"],
                                           item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["investment_way"], item["publish_date"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 股东及出资信息（企业年报信息）
        elif isinstance(item, EntAnnuaShareholderInvestmentInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_annua_shareholder_investment_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"],
                                           item["name"], item["subscribed_amount_sum"],

                                           item["subscribed_amount_sum_currency"], item["subscribed_date"],
                                           item["subscribed_type"],

                                           item["paid_amount_sum"], item["paid_amount_sum_currency"],

                                           item["paid_date"], item["paid_type"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["annua_id"], item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 网站或网店信息（企业年报信息）
        elif isinstance(item, EntAnnuaWebsiteInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_annua_website_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"],
                                           item["categary"], item["name"],
                                           item["url"],
                                           item["create_date"],
                                           item["update_date"], item["empty_ratio"],
                                           item["area_id"], item["data_status"],
                                           item["annua_id"], item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 对外提供保证担保信息（企业年报信息）
        elif isinstance(item, EntAnnuaOutGuaranteeInfoItem):
            try:
                # 插入数据
                sql = "insert into ent_annua_out_guarantee_info values(%s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)"
                self.conn.ping(reconnect=True)
                self.cursors.execute(sql,
                                     [0,
                                      item["order_index"], item["creditor"], item["debtor"],
                                      item["creditor_right_categary"], item["creditor_right_sum"],
                                      item["creditor_right_sum_currency"], item["debtor_period"],
                                      item["guarantee_period"], item["guarantee_type"],
                                      item["create_date"],
                                      item["update_date"], item["area_id"],
                                      item["empty_ratio"], item["data_status"],
                                      item["annua_id"], item["business_license_id"],
                                      ])
                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 分支机构信息（企业年报信息）
        elif isinstance(item, EntBranchInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_branch_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["registration_no"],
                                           item["organization_name"], item["authority"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 变更信息
        elif isinstance(item, EntChangeInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_change_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                if item.get('change_date', None):
                    item["change_date"] = item['change_date'][:10]
                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["change_item"],
                                           item["change_before"], item["change_after"],
                                           item["change_date"],
                                           item["create_date"],
                                           item["update_date"], item["empty_ratio"],
                                           item["area_id"],
                                           item["data_status"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 抽查检查信息
        elif isinstance(item, EntCheckInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_check_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"],
                                           item["check_organization"], item["check_type"],
                                           item["check_date"], item["check_result"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 股权出质信息
        elif isinstance(item, EntEquityPledgedInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_equity_pledged_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"],
                                           item["registration_no"], item["pledgor"],
                                           item["pledgor_certificate_no"], item["equity_number"],
                                           item["pledgee"],
                                           item["pledgee_certificate_no"], item["register_date"],
                                           item["status"], item["publish_time"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 注销信息
        elif isinstance(item, EntEstateMortgageCancelInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_estate_mortgage_cancel_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["cancel_date"],
                                           item["cancel_reason"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"], item["estate_mortgage_id"]
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 动产抵押登记信息
        elif isinstance(item, EntEstateMortgageInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_estate_mortgage_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"],
                                           item["retister_code"], item["retister_date"],
                                           item["retister_organization"], item["guaranteed_number"],
                                           item["guaranteed_amount_currency"],
                                           item["status"], item["publish_date"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 严重违法失信信息
        elif isinstance(item, EntIllegalLostCreditInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_illegal_lost_credit_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"],
                                           item["input_reason"], item["input_date"],
                                           item["input_organization"], item["output_reason"],
                                           item["output_date"],
                                           item["output_organization"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 清算信息
        elif isinstance(item, EntLiquidationInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_liquidation_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["authority"],
                                           item["member"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"]
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 主要人员
        elif isinstance(item, EntMajorPersonInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_major_person_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["name"],
                                           item["department"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"]
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 经营异常信息
        elif isinstance(item, EntOperationExceptionInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_operation_exception_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["order_index"],
                                           item["input_reason"], item["input_date"],
                                           item["input_organization"], item["output_reason"],
                                           item["output_date"],
                                           item["output_organization"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"],
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 股东及出资信息（企业即时信息）
        elif isinstance(item, EntImmediateShareholderInvestmentInfo):

            try:
                # 插入数据
                sql = "insert into ent_immediate_shareholder_investment_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["name"],
                                           item["subscribed_amount_sum"],
                                           item["subscribed_amount_sum_currency"],
                                           item["paid_amount_sum"],
                                           item["paid_amount_sum_currency"],
                                           item["publish_time"],
                                           item["create_date"], item["update_date"],
                                           item["area_id"], item["empty_ratio"],
                                           item["data_status"], item["publish_date"], item["business_license_id"]
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))
        # 认缴明细 企业即时信息
        elif isinstance(item, EntImmediateShareholderSubcribeInfoItem):
            try:
                sql = "insert into ent_immediate_shareholder_subcribe_info values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0,
                                           item["subscribed_type"],
                                           item["subscribed_amount"],
                                           item["subscribed_amount_currency"],
                                           item["subscribed_date"],
                                           item["publish_time"],
                                           item["publish_date"],
                                           item["create_date"],
                                           item["update_date"],
                                           item["area_id"],
                                           item["empty_ratio"],
                                           item["data_status"],
                                           item["business_license_id"],
                                           item["immediate_shareholder_investment_id"],
                                           ])
                self.conn.commit()
            except Exception as e:
                print(e, type(item))
        # 实缴明细（企业即时信息
        elif isinstance(item, EntImmediateShareholderPaidInfoItem):
            try:
                sql = "insert into ent_immediate_shareholder_paid_info values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0,
                                           item["paid_type"],
                                           item["paid_amount"],
                                           item["paid_amount_currency"],
                                           item["paid_date"],
                                           item["create_date"],
                                           item["update_date"],
                                           item["area_id"],
                                           item["empty_ratio"],
                                           item["data_status"],
                                           item["publish_date"],
                                           item["business_license_id"],
                                           item["immediate_shareholder_investment_id"],
                                           ])
                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 认缴明细信息
        elif isinstance(item, EntShareholderSubcribeInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_shareholder_subcribe_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["subscribed_type"],
                                           item["subscribed_amount"], item["subscribed_amount_currency"],
                                           item["subscribed_date"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"], item["shareholder_investment_id"]
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        # 实缴明细信息
        elif isinstance(item, EntShareholderPaidInfoItem):

            try:
                # 插入数据
                sql = "insert into ent_shareholder_paid_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [0, item["paid_type"],
                                           item["paid_amount"], item["paid_amount_currency"],
                                           item["paid_date"],
                                           item["create_date"],
                                           item["update_date"], item["area_id"],
                                           item["empty_ratio"], item["data_status"],
                                           item["business_license_id"], item["shareholder_investment_id"]
                                           ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

        elif isinstance(item, EntAnnuaSocialSecurityInfoItem):
            """
                社保信息
            """
            try:
                # 插入数据
                sql = "insert into ent_annua_social_security_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                self.conn.ping(reconnect=True)
                self.cursors.execute(sql, [
                    0,
                    item['endowment_insurance'],
                    item['unemployment_insurance'],
                    item['medical_insurance'],
                    item['employment_injury_insurance'],
                    item['maternity_insurance'],
                    item['endowment_insurance_base'],
                    item['unemployment_insurance_base'],
                    item['medical_insurance_base'],
                    item['maternity_insurance_base'],
                    item['endowment_insurance_pay_amount'],
                    item['unemployment_insurance_pay_amount'],
                    item['medical_insurance_pay_amount'],
                    item['employment_injury_insurance_pay_amount'],
                    item['maternity_insurance_pay_amount'],
                    item['endowment_insurance_owe_amount'],
                    item['unemployment_insurance_owe_amount'],
                    item['medical_insurance_owe_amount'],
                    item['employment_injury_insurance_owe_amount'],
                    item['maternity_insurance_owe_amount'],
                    item['create_date'],
                    item['update_date'],
                    item['empty_ratio'],
                    item['area_id'],
                    item['data_status'],
                    item['annua_id'],
                    item['business_license_id'],
                ])

                self.conn.commit()
            except Exception as e:
                print(e, type(item))

    # 关闭
    def close_spider(self, spider):
        self.cursors.close()
        self.conn.close()

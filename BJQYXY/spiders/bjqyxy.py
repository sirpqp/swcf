# -*- coding: utf-8 -*-
import re

import scrapy
import pymysql

from furl import furl
from logging import getLogger

from BJQYXY.data_parser.business_license_Info import companybasic
from BJQYXY.data_parser.annua_info import companyannual
from BJQYXY.data_parser.immediate_shareholder_investment_info import companyShareholdersInvestment
from BJQYXY.data_parser.administrative_license_info import licensin_qualification
from BJQYXY.data_parser.check_info import get_check_url
from BJQYXY.data_parser.operation_exception_info import companywarning
from BJQYXY.data_parser.tzr_xinxi import tzrxinxi
from BJQYXY.data_parser.leading_member import majorpersoninfo
from BJQYXY.data_parser.change_info import changeinformation
from BJQYXY.lpop_redis import getRedis
from BJQYXY.get_company_data import *

logger = getLogger('spider')


class BjqyxySpider(scrapy.Spider):
    name = 'bjqyxy'
    allowed_domains = ['gov.cn', 'jsdama.com']
    start_urls = ["http://qyxy.scjgj.beijing.gov.cn/simple/dealSimpleAction!transport_ww.dhtml"]
    offset_num = 0

    def parse(self, response):
        if not response.meta.get('company'):
            company = getRedis()
        else:
            company = response.meta.get('company')
        # 获取主页回来中的参数
        # company = "北京九次方科技发展有限公司"
        try:
            currentTimeMillis = response.xpath('//*[@id="currentTimeMillis"]/@value').extract_first()
            uuid = re.search('document.getElementById\("uuid"\).value="(\w*)"', response.text).group(1)
            creadit_ticket = re.search('var credit_ticket = "(\w*)"', response.text).group(1)
            if not currentTimeMillis:
                logger.error("请打开代理")
                raise RuntimeError("请打开代理")

            # 列表页
            listpage_url = "http://qyxy.scjgj.beijing.gov.cn/es/esAction!entlist.dhtml"
            params = {
                "currentTimeMillis": currentTimeMillis,
                "credit_ticket": creadit_ticket,
                "check_code": 25
            }

            data = {
                "queryStr": company,
                "module": "",
                "times": "",
                "createTicket": "",
                "uuid": uuid,
                "idFlag": "qyxy"
            }
            # 进入企业列表页
            listpage_url += "?currentTimeMillis={currentTimeMillis}&credit_ticket={credit_ticket}&check_code={check_code}".format(
                **params)
            yield scrapy.FormRequest(listpage_url, formdata=data, callback=self.get_list_page, meta={'company': company})
        except:
            response.meta['company'] = company
            yield scrapy.Request(url=response.url, dont_filter=True, meta=response.meta)

        yield scrapy.Request(url=self.start_urls[0], dont_filter=True)

    def get_list_page(self, response):
        """
        列表页解析
        """
        if "您可能频繁重复请求" in response.text:
            time.sleep(0.5)
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse, dont_filter=True, meta=response.meta)
            return None

        href_urls = response.xpath("//h3/@onclick/..")
        if href_urls:
            for i in href_urls:
                try:
                    detail_url = i.xpath("./@onclick").extract_first()
                    detailurl = "http://qyxy.scjgj.beijing.gov.cn" + detail_url.split("'")[1]
                    querystr = ''.join(i.xpath("./span[1]//text()").extract())
                    if '（开业）' in querystr:
                        querystr = querystr.split('（开业）')[0].strip()
                    elif '（注销）' in querystr:
                        querystr = querystr.split('（注销）')[0].strip()
                    elif '（吊销）' in querystr:
                        querystr = querystr.split('（吊销）')[0].strip()

                    # 公司去重
                    con = pymysql.connect(
                        host=self.settings['HOST'], port=self.settings['PORT'],
                        user=self.settings['USER'], password=self.settings['PASSWORD'],
                        database=self.settings['NAME'], charset="utf8"
                    )

                    # 使用cursor()方法获取操作游标
                    cursor = con.cursor()
                    # 查询公司是否爬取过

                    cursor.execute(("SELECT 1 from ent_business_license_info where name='%s'" % querystr))
                    company_exist = cursor.fetchone()
                    cursor.close()
                    con.close()
                    if not company_exist:
                        print("\t", querystr)
                        yield scrapy.Request(detailurl, callback=self.get_details_page, meta={'company': querystr})
                    else:
                        print(querystr, "已经入库")
                except:
                    pass

    def get_details_page(self, response):

        # 基本参数
        try:
            entId = response.xpath("//body/@onload").extract_first().split("','")[1]
        except:
            time.sleep(0.5)
            yield scrapy.Request(response.url, callback=self.get_details_page, meta=response.meta, dont_filter=True)
            return None

        if entId == "":
            time.sleep(0.5)
            yield scrapy.Request(response.url, callback=self.get_details_page, meta=response.meta, dont_filter=True)
        else:
            params = {
                "entId": entId,
                "flag_num": 0,
                "clear": "true",
                "timeStamp": int(time.time() * 1000)
            }

            if params['entId'] == "":
                yield scrapy.Request(response.url, callback=self.get_details_page, meta=response.meta, dont_filter=True)
                return None

            company_date = GetCompanyDate(response.meta['company'])
            if company_date:
                td_list = response.xpath("//table[@class='f-lbiao'][1]//tr/td//text()")
                if td_list:
                    for idx, i in enumerate(td_list):
                        try:
                            approval_date = td_list[idx + 1].extract().strip()
                            approval_date = datetime.datetime.strptime(approval_date, '%Y-%m-%d')

                        except:
                            approval_date = ''
                    # print(approval_date)
                    if company_date == approval_date:
                        return

            # 基本信息
            yield companybasic(response)

            # 企业年报(完成)
            f_url = furl("http://qyxy.scjgj.beijing.gov.cn/entPub/entPubAction!getTabForNB_new.dhtml")
            f_url.args = params
            # 请求年报网页
            yield scrapy.Request(f_url.url, callback=companyannual, meta=response.meta)

            # 股东出资信息(完成)
            f_url = furl("http://qyxy.scjgj.beijing.gov.cn/newChange/newChangeAction!getTabForNB_new.dhtml")
            params['flag_num'] = 1
            f_url.args = params
            yield scrapy.Request(f_url.url, callback=companyShareholdersInvestment, meta=response.meta)
            #
            # 许可资质(完成)
            data_count = response.xpath("//li[@id='TabbedPanelsTab_01']/span/text()").extract_first()
            # 证明没有数据
            if data_count and int(data_count) > 0:
                params = {
                    "reg_bus_ent_id": entId,
                    "info_categ": '01',
                    "vchr_bmdm": ""
                }
                f_url = furl("http://qyxy.scjgj.beijing.gov.cn/newChange/newChangeAction!getGj.dhtml")
                f_url.args = params
                response.meta['ent_id'] = entId
                yield scrapy.Request(f_url.url, callback=licensin_qualification, meta=response.meta)

            # 警示信息(经营人异常信息)(完成)
            yield companywarning(response)

            # 提示信息 (抽查检查信息) (完成)
            yield get_check_url(response)

            # 固定及出资信息，认缴信息，实缴信息
            yield tzrxinxi(response)

            # 变更信息
            yield changeinformation(response)

            # 主要人员
            yield majorpersoninfo(response)

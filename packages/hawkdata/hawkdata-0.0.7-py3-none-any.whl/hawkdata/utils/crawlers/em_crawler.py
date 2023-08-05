# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np

import logging, time, random, json, retrying, math, hashlib, re

from datetime import datetime
from operator import itemgetter
from functools import lru_cache

from hawkdata.utils.crawlers import WebCrawlerBase


class EmCrawler(WebCrawlerBase):

    HOME_PAGE = 'https://fund.eastmoney.com'

    URL_MUTUAL_FUND_DESC = \
        'https://fund.eastmoney.com/js/fundcode_search.js'

    URL_FUND_NAV = \
        'http://fund.eastmoney.com/pingzhongdata/%s.js'
    RE_FUND_UNIT_NAV = re.compile('Data_netWorthTrend\s*=\s*(\[.*?\]);')
    RE_FUND_ACC_NAV = re.compile('Data_ACWorthTrend\s*=\s*(\[.*?\]);')
    RE_MONEY_FUND_INCOME = \
        re.compile('Data_millionCopiesIncome\s*=\s*(\[.*?\]);')
    RE_MONEY_FUND_SEVEN_DAYS_YEARLY_ROE = \
        re.compile('Data_sevenDaysYearIncome\s*=\s*(\[.*?\]);')

    # 'FHSP' 为 '分红送配' 缩写
    URL_FUND_FHSP = \
        'https://fundf10.eastmoney.com/fhsp_%s.html'
    RE_DIVIDEND_TABLE = re.compile('每份分红')
    RE_DIVIDEND_VALUE = re.compile('([0-9]+\.[0-9]*)')
    RE_SPLIT_TABLE = re.compile('拆分折算日')
    RE_SPLIT_VALUE = re.compile('[0-9]+:([0-9]+\.?[0-9]*)')

    URL_US_STOCK_HOMEPAGE = \
        'https://quote.eastmoney.com/us/%s.html'
    RE_STOCK_CODE_IN_HOMEPAGE = \
        re.compile('var\s+quotecode\s*=\s*"([0-9a-zA-Z.]+)"\s*;')

    URL_US_STOCK_KLINE_DAILY = \
        'https://push2his.eastmoney.com/api/qt/stock/kline/get'

    __instance = None

    def __new__(self, *args, **kw):

        if self.__instance is None:
            self.__instance = object.__new__(self, *args, **kw)

        return self.__instance

    def __init__(self):

        pass

    def __extract_money_fund_income_from_res_text(self, res_text):

        money_fund_income_search_result = \
            self.RE_MONEY_FUND_INCOME.search(res_text)
        if money_fund_income_search_result is None:
            return {}

        money_fund_income_search_result_text = \
            money_fund_income_search_result.group(1)
        money_fund_income_search_result_json = \
            json.loads(money_fund_income_search_result_text)

        # 按照时间戳排序
        money_fund_income_search_result_json = \
            sorted(money_fund_income_search_result_json,
                   key = lambda item: item[0])

        return money_fund_income_search_result_json

    def __extract_money_fund_seven_days_yearly_roe_from_res_text(self,
                                                                 res_text):

        money_fund_seven_days_yearly_roe_search_result = \
            self.RE_MONEY_FUND_SEVEN_DAYS_YEARLY_ROE.search(res_text)
        if money_fund_seven_days_yearly_roe_search_result is None:
            return {}

        money_fund_seven_days_yearly_roe_search_result_text = \
            money_fund_seven_days_yearly_roe_search_result.group(1)
        money_fund_seven_days_yearly_roe_result_json = \
            json.loads(money_fund_seven_days_yearly_roe_search_result_text)

        return money_fund_seven_days_yearly_roe_result_json

    def __extract_unit_nav_from_res_text(self, res_text):

        fund_unit_nav_search_result = self.RE_FUND_UNIT_NAV.search(res_text)
        if fund_unit_nav_search_result is None:
            return {}

        fund_unit_nav_search_result_text = fund_unit_nav_search_result.group(1)
        fund_unit_nav_search_result_json = \
            json.loads(fund_unit_nav_search_result_text)

        for item in fund_unit_nav_search_result_json:

            if 'unitMoney' not in item:
                continue

            unit_money = item['unitMoney']
            del item['unitMoney']

            # 将接口返回的表示净值的 Key 'y' 重命名成 'nav'
            item['unit_nav'] = item.pop('y')

            # 将接口返回的 UNIX Timestamp 转换成 Date 类型
            item['nav_date'] = \
                datetime.fromtimestamp(item['x']/1e3).date().strftime(
                    '%Y-%m-%d')
            del item['x']

            # 将接口返回的参数 equityReturn 删除，因为用不到。
            # 此外，且该值不完全正确，部分值未能正确计入分红送配带来的影响。
            del item['equityReturn']

        return fund_unit_nav_search_result_json

    def __extract_acc_nav_from_res_text(self, res_text):

        fund_acc_nav_search_result = self.RE_FUND_ACC_NAV.search(res_text)
        if fund_acc_nav_search_result is None:
            return {}

        fund_acc_nav_search_result_text = fund_acc_nav_search_result.group(1)
        fund_acc_nav_search_result_json = \
            json.loads(fund_acc_nav_search_result_text)

        acc_nav_list = []
        for item in fund_acc_nav_search_result_json:

            if len(item) < 2:
                continue

            nav_date = \
                datetime.fromtimestamp(item[0]/1e3).date().strftime(
                    '%Y-%m-%d')
            acc_nav_list.append({
                'nav_date': nav_date,
                'acc_nav': item[1]
            })

        return acc_nav_list

    def __extract_dividend_value_in_string(self, s):

        search_result = self.RE_DIVIDEND_VALUE.search(s)
        if search_result is None:
            return None

        return search_result.group(1)

    def __extract_split_value_in_string(self, s):

        search_result = self.RE_SPLIT_VALUE.search(s)
        if search_result is None:
            return None

        return search_result.group(1)

    def __extract_dividend_df_from_res_text(self, res_text):

        dividend_df = pd.read_html(res_text, match=self.RE_DIVIDEND_TABLE)[0]

        if self.RE_DIVIDEND_VALUE.search(dividend_df['每份分红'].iloc[0]) \
                is None:
            return None

        dividend_df['每份分红'] = dividend_df['每份分红'].apply(
            self.__extract_dividend_value_in_string)

        return dividend_df

    def __extract_split_df_from_res_text(self, res_text):

        split_df = pd.read_html(res_text, match=self.RE_SPLIT_TABLE)[0]

        if self.RE_SPLIT_VALUE.search(split_df['拆分折算比例'].iloc[0]) is None:
            return None

        split_df['拆分折算比例'] = split_df['拆分折算比例'].apply(
            self.__extract_split_value_in_string)

        return split_df

    def __query_fund_fhsp_page_as_text(self, fund_code):

        res = self._crawl(self.URL_FUND_FHSP % (fund_code))
        res_text = res.text

        return res_text

    @lru_cache(maxsize=16384, typed=False)
    def __extract_em_stock_code_from_us_stock_homepage(self, stock_code):

        stock_url = self.URL_US_STOCK_HOMEPAGE % (stock_code)

        stock_home_res = self._crawl(stock_url)
        stock_home_res_text = stock_home_res.text

        em_stock_code_search_result = \
            self.RE_STOCK_CODE_IN_HOMEPAGE.search(stock_home_res_text)
        if em_stock_code_search_result is None:
            return None
        em_stock_code = em_stock_code_search_result.group(1)

        return em_stock_code

    def mutual_fund_desc(self):

        res = self._crawl(self.URL_MUTUAL_FUND_DESC)
        res_text = res.text

        res_head_idx = res_text.index('[[')
        res_tail_idx = res_text.index(']];')

        valid_text = res_text[res_head_idx:res_tail_idx+2]

        return json.loads(valid_text)

    def mutual_fund_unit_and_acc_nav(self, fund_code):

        res = self._crawl(self.URL_FUND_NAV % (fund_code))
        res_text = res.text

        # 尝试获取货币基金的万份收益信息
        money_fund_income_list = \
            self.__extract_money_fund_income_from_res_text(res_text)

        # 若未获取到货币基金万份收益信息，则走非货币基金处理逻辑
        if money_fund_income_list is None or \
                len(money_fund_income_list) <= 0:

            # 标记该基金为非货币基金
            is_money_fund = False

            # 获取非货币基金单位净值信息
            fund_unit_nav_list = \
                self.__extract_unit_nav_from_res_text(res_text)

            # 获取非货币基金累计净值信息
            fund_acc_nav_list = \
                self.__extract_acc_nav_from_res_text(res_text)

            return fund_unit_nav_list, fund_acc_nav_list, is_money_fund

        # 若获取到货币基金万份收益信息，则走货币基金处理逻辑

        # 标记该基金为货币基金
        is_money_fund = True

        # 尝试获取货币基金七日年化收益率信息
        money_fund_seven_days_yearly_roe_list = \
            self.__extract_money_fund_seven_days_yearly_roe_from_res_text(
                res_text)
        money_fund_seven_days_yearly_roe_dict = \
            {item[0]: item[1] for item in money_fund_seven_days_yearly_roe_list}

        acc_nav = 1.0
        adj_nav = 1.0
        fund_unit_nav_list = []

        for item in money_fund_income_list:

            # 接口返回的内数组应含有两个元素，第一个是时间戳，第二个是万份收益
            if len(item) != 2:
                continue

            # 获取净值日期
            ts = item[0]
            nav_date = \
                datetime.fromtimestamp(ts/1e3).date().strftime('%Y-%m-%d')

            yield_per_ten_thousand = item[1]
            yearly_roe = \
                money_fund_seven_days_yearly_roe_dict.get(ts, np.NaN)
            if pd.isnull(yearly_roe) is False:
                yearly_roe = yearly_roe / 1e2

            # 将万份收益还原为每份收益
            unit_yield = yield_per_ten_thousand / 1e4

            acc_nav = acc_nav + unit_yield

            prev_adj_nav = adj_nav
            adj_nav = adj_nav + (adj_nav * unit_yield)
            adj_nav_return = (adj_nav / prev_adj_nav) - 1

            # 货币基金净值永远为 1
            fund_unit_nav_list.append({
                'nav_date': nav_date,
                'unit_nav': 1.0,
                'unit_yield': yield_per_ten_thousand,
                'yearly_roe': yearly_roe,
                'acc_nav': acc_nav,
                'adj_nav': adj_nav,
                'adj_nav_return': adj_nav_return
            })

        return fund_unit_nav_list, None, is_money_fund

    def mutual_fund_dividend_and_split(self, fund_code):

        fhsp_page_text = self.__query_fund_fhsp_page_as_text(fund_code)

        dividend_df = self.__extract_dividend_df_from_res_text(fhsp_page_text)
        if dividend_df is not None:
            dividend_df = dividend_df.drop(['年份'], axis=1)
            dividend_df = dividend_df.rename(columns={
                '权益登记日': 'eqy_record_date',
                '除息日': 'ex_date',
                '每份分红': 'dvd_per_sh',
                '分红发放日': 'pay_date'
            })

        split_df = self.__extract_split_df_from_res_text(fhsp_page_text)
        if split_df is not None:
            split_df = split_df.drop(['年份'], axis=1)
            split_df = split_df.rename(columns={
                '拆分折算日': 'split_date',
                '拆分类型': 'split_type',
                '拆分折算比例': 'split_inc'
            })

        return dividend_df, split_df

    def stock_us_price_hist(self, stock_code,
                            start_date=None, end_date=None,
                            adj_mode=''):

        if start_date is None:
            start_date = '0'
        if end_date is None:
            end_date = '29991231'

        em_stock_code = self.__extract_em_stock_code_from_us_stock_homepage(
            stock_code)

        adj_mode_dict = {
            'qfq': '1',
            'hfq': '2'
        }

        request_params = {
            'secid': em_stock_code,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f59,f60,f61',
            'klt': '101',
            'beg': start_date,
            'end': end_date,
            'fqt': adj_mode_dict.get(adj_mode, '0'),
            '_': str(int(time.time() * 1000))
        }
        price_res = self._crawl(self.URL_US_STOCK_KLINE_DAILY,
                                params=request_params)
        price_res_text = price_res.text
        price_res_json = json.loads(price_res_text)

        kline_data_list = price_res_json['data']['klines']

        price_df = pd.DataFrame([item.split(',') for item in kline_data_list])
        price_df.columns = [
            'txn_date',
            'open',
            'close',
            'high',
            'low',
            'volume',
            'amount',
            'pct_change',
            'change',
            'turnover'
        ]

        return price_df

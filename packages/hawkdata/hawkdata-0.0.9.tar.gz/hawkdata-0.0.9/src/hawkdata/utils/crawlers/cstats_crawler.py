# -*- coding:utf-8 -*-


import pandas as pd
import numpy as np
import requests
import time, json, urllib.parse

from datetime import datetime

from hawkdata.utils.crawlers import WebCrawlerBase


class CStatsCrawler(WebCrawlerBase):

    __QUERY_URL = 'https://data.stats.gov.cn/easyquery.htm'

    __DB_CODE_MACRO_MONTHLY     = 'hgyd'
    __DB_CODE_MACRO_QUARTERLY   = 'hgjd'
    __DB_CODE_MACRO_YEARLY      = 'hgnd'

    __DATE_FORMAT               = '%Y-%m-%d'

    __instance = None

    def __new__(self, *args, **kw):

        if self.__instance is None:
            self.__instance = object.__new__(self, *args, **kw)

        return self.__instance

    def __init__(self):

        pass

    def __get_data_from_query_url(self, db_code, metrix_code, time_range,
                                  use_exact_value=False,
                                  df_columns=['datetime', 'value']):

        param_wds = []
        param_dfwds = [
            {
                "wdcode": "sj",
                "valuecode": time_range
            },
            {
                "wdcode": "zb",
                "valuecode": metrix_code
            }
        ]

        request_params = {
            'm': 'QueryData',
            'dbcode': db_code,
            'rowcode': 'zb',
            'colcode': 'sj',
            'wds': json.dumps(param_wds),
            'dfwds': json.dumps(param_dfwds),
            'k1': str(int(time.time() * 1000))
        }

        res = self._crawl(self.__QUERY_URL, params=request_params,
                          ssl_verify=False)
        res_text = res.text

        res_json = json.loads(res_text)
        if res_json is None:
            return None

        returndata = res_json.get('returndata', None)
        if returndata is None:
            return None

        datanodes = returndata.get('datanodes', None)
        if datanodes is None or len(datanodes) <= 0:
            return None

        data_list = []
        for node in datanodes:

            code_area = node.get('code', None)
            if code_area is None:
                continue

            splitted_codes = code_area.split('.')
            if len(splitted_codes) < 3:
                continue

            # 确定日期时间值
            datetime_str = splitted_codes[2]

            data_area = node.get('data', None)
            if data_area is None:
                continue

            has_data = data_area.get('hasdata', False)
            if has_data is False:
                continue

            # 确定日期时间对应的指标值
            if use_exact_value is True:
                data_value = data_area.get('data', None)
            else:
                data_value = None
                data_value_str = data_area.get('strdata', None)
                if data_value_str is not None and data_value_str != '':
                    data_value = float(data_value_str)

            if data_value is None:
                continue

            data_list.append([datetime_str, data_value])

        result_df = pd.DataFrame(data=data_list,
                                  columns=df_columns)

        return result_df

    def __get_date_str_from_quarter_with_alphabet(self, quarter_str):

        if quarter_str is None or len(quarter_str) <= 0:
            return None

        str_year = quarter_str[:-1]
        str_quarter_mark = quarter_str[-1].upper()

        if str_quarter_mark == 'A':
            str_date = '03-31'
        elif str_quarter_mark == 'B':
            str_date = '06-30'
        elif str_quarter_mark == 'C':
            str_date = '09-30'
        elif str_quarter_mark == 'D':
            str_date = '12-31'
        else:
            return None

        str_year_date = '%s-%s' % (str_year, str_date)

        return str_year_date

    def macro_china_yearly_gdp(self):

        yearly_gdp_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_YEARLY,
                                           'A020101', '1978-',
                                           df_columns=['year', 'gdp'])
        yearly_gdp_df = yearly_gdp_df.astype({
            'year': 'int',
            'gdp': 'float64'
        })

        return yearly_gdp_df.sort_values(by=['year'], ascending=True,
                                         ignore_index=True)

    def macro_china_yearly_gdp_idx(self):

        yearly_gdp_idx_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_YEARLY,
                                           'A02020101', '1978-',
                                           df_columns=['year', 'gdp_idx'])

        yearly_gdp_idx_df = yearly_gdp_idx_df.astype({
            'year': 'int',
            'gdp_idx': 'float64'
        })

        return yearly_gdp_idx_df.sort_values(by=['year'], ascending=True,
                                             ignore_index=True)

    def macro_china_yearly_gdp_index(self):

        yearly_gdp_index_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_YEARLY,
                                           'A02020202', '1978-',
                                           df_columns=['year', 'gdp_index'])

        yearly_gdp_index_df = yearly_gdp_index_df.astype({
            'year': 'int',
            'gdp_index': 'float64'
        })

        return yearly_gdp_index_df.sort_values(by=['year'], ascending=True,
                                               ignore_index=True)

    def macro_china_quarterly_gdp(self):

        quarterly_gdp_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_QUARTERLY,
                                           'A010101', '1992-',
                                           df_columns=['date', 'gdp'])

        quarterly_gdp_df['date'] = quarterly_gdp_df['date'].apply(
            lambda x: self.__get_date_str_from_quarter_with_alphabet(x))

        quarterly_gdp_df = quarterly_gdp_df.astype({
            'date': 'string',
            'gdp': 'float64'
        })

        quarterly_gdp_df['date'] = quarterly_gdp_df['date'].apply(
            lambda x: datetime.strptime(x, self.__DATE_FORMAT))

        return quarterly_gdp_df.sort_values(by=['date'], ascending=True,
                                            ignore_index=True)

    def macro_china_quarterly_gdp_idx(self):

        quarterly_gdp_idx_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_QUARTERLY,
                                           'A010301', '1993-',
                                           df_columns=['date', 'gdp_idx'])

        quarterly_gdp_idx_df['date'] = quarterly_gdp_idx_df['date'].apply(
            lambda x: self.__get_date_str_from_quarter_with_alphabet(x))

        quarterly_gdp_idx_df = quarterly_gdp_idx_df.astype({
            'date': 'string',
            'gdp_idx': 'float64'
        })

        quarterly_gdp_idx_df['date'] = quarterly_gdp_idx_df['date'].apply(
            lambda x: datetime.strptime(x, self.__DATE_FORMAT))

        return quarterly_gdp_idx_df.sort_values(by=['date'], ascending=True,
                                                ignore_index=True)

    def macro_china_yearly_cpi_idx(self):

        yearly_cpi_idx_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_YEARLY,
                                           'A090101', '1951-',
                                           df_columns=['year', 'cpi_idx'])

        yearly_cpi_idx_df = yearly_cpi_idx_df.astype({
            'year': 'int',
            'cpi_idx': 'float64'
        })

        return yearly_cpi_idx_df.sort_values(by=['year'], ascending=True,
                                             ignore_index=True)

    def macro_china_yearly_cpi_fixed_base_idx(self):

        yearly_cpi_idx_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_YEARLY,
                                           'A090201', '1978-',
                                           df_columns=['year', 'cpi_index'])

        yearly_cpi_idx_df = yearly_cpi_idx_df.astype({
            'year': 'int',
            'cpi_index': 'float64'
        })

        return yearly_cpi_idx_df.sort_values(by=['year'], ascending=True,
                                             ignore_index=True)

    def macro_china_monthy_cpi_idx(self):

        cpi_idx_1987_to_2015_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_MONTHLY,
                                           'A01010201', '1987-',
                                           df_columns=['month', 'cpi_idx'])
        cpi_idx_2016_to_now_df = \
            self.__get_data_from_query_url(self.__DB_CODE_MACRO_MONTHLY,
                                           'A01010101', '2016-',
                                           df_columns=['month', 'cpi_idx'])

        cpi_idx_full_df = cpi_idx_1987_to_2015_df.append(cpi_idx_2016_to_now_df,
                                                         ignore_index=True)
        cpi_idx_full_df = cpi_idx_full_df.astype({
            'month': 'int',
            'cpi_idx': 'float64'
        })

        return cpi_idx_full_df.sort_values(by=['month'], ascending=True,
                                           ignore_index=True)

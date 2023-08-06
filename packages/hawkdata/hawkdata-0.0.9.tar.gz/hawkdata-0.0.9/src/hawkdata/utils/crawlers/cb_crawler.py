# -*- coding:utf-8 -*-

import json, re
import pandas as pd

from tqdm import tqdm

from hawkdata.utils.datasetx import datasetx as dsx
from hawkdata.utils.crawlers import WebCrawlerBase


class CbCrawler(WebCrawlerBase):

    CBOND_STANDARD_TERM_API_URL = \
        'https://yield.chinabond.com.cn/cbweb-mn/yc/ycDetail'

    CBOND_ID_DICT = {
        '1': {
            'curve_name': '中债国债收益率曲线',
            'yc_defid': '2c9081e50a2f9606010a3068cae70001'
        },
        '2': {
            'curve_name': '中债中短期票据收益率曲线(AAA)',
            'yc_defid': '2c9081880fa9d507010fb8505b393fe7'
        },
        '3': {
            'curve_name': '中债商业银行普通债收益率曲线(AAA)',
            'yc_defid': '2c9081e9259b766a0125be8b5115149f'
        },
        '4': {
            'curve_name': '中债企业债收益率曲线(AAA)',
            'yc_defid': '2c9081e50a2f9606010a309f4af50111'
        },
        '5': {
            'curve_name': '中债中资美元债收益率曲线(A)',
            'yc_defid': 'ff8080816a064b08016a0bdbb6400011'
        }
    }

    RE_YIELD_TABLE = re.compile('标准期限')

    __instance = None

    def __new__(self, *args, **kw):

        if self.__instance is None:
            self.__instance = object.__new__(self, *args, **kw)

        return self.__instance

    def __init__(self):

        pass

    def __get_cbond_yield_data_with_standard_term(self, yc_defid, worktime):

        request_params = {
            'workTime': worktime,
            'ycDefIds': yc_defid,
            'zblx': 'txy',
            'dxbj': '0',
            'qxlx': '0,',
            'yqqxN': 'N',
            'yqqxK': 'K',
            'wrjxCBFlag': '0',
            'locale': 'zh_CN'
        }

        res = self._crawl(self.CBOND_STANDARD_TERM_API_URL, method='POST',
                          params=request_params)
        res_text = res.text
        try:
            curve_name = \
                pd.read_html(res_text, attrs={'class': 't1'})[0].iloc[0][1]
            yield_df_list = pd.read_html(res_text, attrs={'class': 'tablelist'})
        except Exception as e:
            return None, None

        return curve_name, yield_df_list[0]

    def __get_yc_defid_list_from_id_list(self, id_list):

        yc_defid_list = []

        for id_item in id_list:

            dict_item = self.CBOND_ID_DICT.get(id_item, None)
            if dict_item is None:
                continue

            yc_defid = dict_item.get('yc_defid', None)
            if yc_defid is None:
                continue

            yc_defid_list.append(yc_defid)

        return yc_defid_list

    def __get_cbond_curve_yield_df_from_raw_data(self, curve_raw_data):

        for item in curve_raw_data:

            series_data = item.get('seriesData', None)
            if series_data is None:
                continue

            yc_def_name = item['ycDefName']
            worktime = item['worktime']

            for serie_item in series_data:

                if len(serie_item) < 2:
                    continue

    def cbond_curve_yield(self, id_list, date_list):

        RET_DF_COLUMN = ['curve_name', 'date', '3_month', 'half_year', '1_year',
                         '3_year', '5_year', '7_year', '10_year', '20_year',
                         '30_year']
        ret_df = pd.DataFrame(columns=RET_DF_COLUMN)

        yc_defid_list = self.__get_yc_defid_list_from_id_list(id_list)

        pbar = tqdm(total=len(yc_defid_list)*len(date_list), unit='part')

        for item_yc_defid in yc_defid_list:

            for item_date in date_list:

                pbar.update(1)

                curve_name, yield_df = \
                    self.__get_cbond_yield_data_with_standard_term(
                        item_yc_defid, str(item_date))
                if yield_df is None:
                    continue

                yield_df = yield_df.rename(columns={
                    0: 'std_term',
                    1: 'yield'
                })
                yield_df = yield_df[1:]
                yield_dict = dict(yield_df.values)

                ret_df = ret_df.append({
                    'curve_name': curve_name,
                    'date': str(item_date),
                    '3_month': yield_dict.get('0.25y', None),
                    'half_year': yield_dict.get('0.5y', None),
                    '1_year': yield_dict.get('1.0y', None),
                    '3_year': yield_dict.get('3.0y', None),
                    '5_year': yield_dict.get('5.0y', None),
                    '7_year': yield_dict.get('7.0y', None),
                    '10_year': yield_dict.get('10.0y', None),
                    '20_year': yield_dict.get('20.0y', None),
                    '30_year': yield_dict.get('30.0y', None)
                }, ignore_index=True)

        pbar.close()

        return ret_df

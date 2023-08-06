# -*- coding:utf-8 -*-


import pandas as pd
import numpy as np
import requests
import time, json, urllib.parse, math

from tqdm import tqdm
from datetime import datetime
from pandarallel import pandarallel
from cachetools import cached, TTLCache

from hawkdata.utils.crawlers import WebCrawlerBase


class CnIdxCrawler(WebCrawlerBase):

    __BASE_URL              = 'http://www.cnindex.com.cn'

    __QUERY_INDEX_ITEM_API  = '%s/index/indexList' % (__BASE_URL)
    __QUERY_INDEX_INTRO_API = '%s/index-intro' % (__BASE_URL)

    __INDEX_TYPE_CODE_DICT  = {
        '100': '规模',
        '101': '行业',
        '102': '风格',
        '103': '主题',
        '104': '策略',
        '105': '综合',
        '106': '债券',
        '107': '基金'
    }

    __instance = None

    def __new__(self, *args, **kw):

        if self.__instance is None:
            self.__instance = object.__new__(self, *args, **kw)

        return self.__instance

    def __init__(self):

        pandarallel.initialize(nb_workers=4, progress_bar=True, verbose=0)

    def __get_idx_basic_info_df(self, idx_type_code):

        ROWS_PER_PAGE = 1000

        request_params = {
            'channelCode': idx_type_code,
            'rows': ROWS_PER_PAGE,
            'pageNum': None
        }

        page = 1
        page_count = 1
        idx_basic_info_list = []

        while page <= page_count:

            request_params['pageNum'] = page

            res = self._crawl(self.__QUERY_INDEX_ITEM_API, params=request_params)
            res_text = res.text
            res_json = json.loads(res_text)

            res_code = res_json.get('code', None)
            if res_code is None or res_code != 200:
                page = page + 1
                continue

            res_data = res_json.get('data', None)
            if res_data is None:
                page = page + 1
                continue

            idx_total = res_data.get('total', None)
            if idx_total is not None:
                page_count = math.ceil(idx_total/ROWS_PER_PAGE)

            idx_rows = res_data.get('rows', [])
            for idx_item in idx_rows:

                idx_code = idx_item.get('indexcode', None)
                if idx_code is None:
                    continue

                idx_cn_name = idx_item.get('indexname', None)
                idx_en_name = idx_item.get('indexename', None)
                idx_full_cn_name = idx_item.get('indexfullcname', None)
                idx_full_en_name = idx_item.get('indexfullename', None)
                idx_con_num = idx_item.get('samplesize', None)
                idx_class_classify = self.__INDEX_TYPE_CODE_DICT[idx_type_code]

                idx_basic_info_list.append([idx_code, idx_cn_name, idx_en_name,
                                            idx_con_num, idx_full_cn_name,
                                            idx_full_en_name, '深证指数',
                                            idx_class_classify, '人民币'])

            page = page + 1

        df_columns = ['index_code', 'index_sname', 'index_ename', 'con_num',
                      'index_c_fullname', 'index_e_fullname', 'class_series',
                      'class_classify', 'class_currency']
        idx_basic_info_df = pd.DataFrame(data=idx_basic_info_list,
                                         columns=df_columns)

        return idx_basic_info_df

    @cached(cache=TTLCache(maxsize=8192, ttl=600))
    def __get_idx_intro_dict_by_id(self, idx_id):

        request_params = {
            'indexcode': idx_id
        }

        request_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }

        res = self._crawl(self.__QUERY_INDEX_INTRO_API, params=request_params,
                          headers=request_headers)
        res_text = res.text
        res_json = json.loads(res_text)

        res_code = res_json.get('code', None)
        if res_code is None or res_code != 200:
            return None

        res_data = res_json.get('data', None)

        return res_data

    def _get_idx_base_point_by_id(self, idx_id):

        idx_intro_dict = self.__get_idx_intro_dict_by_id(idx_id)

        return idx_intro_dict.get('jd', None)

    def _get_idx_base_date_by_id(self, idx_id):

        idx_intro_dict = self.__get_idx_intro_dict_by_id(idx_id)

        return idx_intro_dict.get('jr', None)

    def _get_idx_online_date_by_id(self, idx_id):

        idx_intro_dict = self.__get_idx_intro_dict_by_id(idx_id)

        return idx_intro_dict.get('fbrq', None)

    def aindex_cni_stock_desc(self):

        full_idx_df = pd.DataFrame()
        pbar = tqdm(total=len(self.__INDEX_TYPE_CODE_DICT), unit='page')

        for idx_type_code in self.__INDEX_TYPE_CODE_DICT:

            idx_type_name = self.__INDEX_TYPE_CODE_DICT[idx_type_code]

            idx_basic_info_df = self.__get_idx_basic_info_df(idx_type_code)
            if idx_basic_info_df is None or len(idx_basic_info_df) <= 0:
                continue

            full_idx_df = full_idx_df.append(idx_basic_info_df,
                                             ignore_index=True)

            pbar.update(1)

        append_func = lambda x: pd.Series([
            self._get_idx_base_point_by_id(x['index_code']),
            self._get_idx_base_date_by_id(x['index_code']),
            self._get_idx_online_date_by_id(x['index_code'])
        ])
        full_idx_df[['base_point', 'base_date', 'online_date']] = \
            full_idx_df.parallel_apply(append_func, axis=1)

        return full_idx_df

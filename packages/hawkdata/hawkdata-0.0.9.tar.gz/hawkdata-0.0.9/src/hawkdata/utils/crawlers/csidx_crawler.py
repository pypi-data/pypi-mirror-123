# -*- coding:utf-8 -*-


import json
import pandas as pd
import numpy as np

from tqdm import tqdm
from cachetools import cached, TTLCache
from pandarallel import pandarallel
from datetime import datetime

from hawkdata.utils.crawlers import WebCrawlerBase


class CsIdxCrawler(WebCrawlerBase):

    __BASE_URL              = 'https://www.csindex.com.cn'

    __TAG_LIST_API          = \
        '%s/csindex-home/index-list/tag-list' % (__BASE_URL)
    __QUERY_INDEX_ITEM_API  = \
        '%s/csindex-home/index-list/query-index-item' % (__BASE_URL)

    __QUERY_INDEX_BASIC_API_TEMPLATE    = \
        '%s/csindex-home/indexInfo/index-basic-info' % (__BASE_URL)

    __DATE_FORMAT = '%Y-%m-%d'

    __instance = None

    def __new__(self, *args, **kw):

        if self.__instance is None:
            self.__instance = object.__new__(self, *args, **kw)

        return self.__instance

    def __init__(self):

        pandarallel.initialize(nb_workers=4, progress_bar=True, verbose=0)

    @cached(cache=TTLCache(maxsize=1, ttl=300))
    def __get_idx_tag_list(self):

        res = self._crawl(self.__TAG_LIST_API, headers={
            'Referer': 'https://www.csindex.com.cn/zh-CN/indices/index?class_10=10'
        })
        res_text = res.text
        res_json = json.loads(res_text)

        res_code = res_json.get('code', None)
        if res_code is None or res_code != '200':
            return None

        res_data = res_json.get('data', None)
        if res_data is None or len(res_data) <= 0:
            return None

        return res_data

    def __get_idx_series_list(self):

        idx_tag_list = self.__get_idx_tag_list()

        idx_series_list = idx_tag_list.get('indexSeriesList', None)
        if idx_series_list is None:
            return []

        return idx_series_list

    def __get_idx_basic_info_df_by_serie_id(self, serie_id):

        PAGE_SIZE = 500

        request_data_body = {
            "sorter": {
                "sortField": "null",
                "sortOrder": None
            },
            "pager": {
                "pageNum": None,
                "pageSize": PAGE_SIZE
            },
            "indexFilter": {
                "ifCustomized": None,
                "ifTracked": None,
                "ifWeightCapped": None,
                "indexCompliance": None,
                "hotSpot": None,
                "indexClassify": None,
                "currency": None,
                "region": None,
                "indexSeries": [serie_id],
                "undefined": None
            }
        }

        request_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8'
        }

        page = 1
        page_count = 1
        idx_basic_info_list = []

        while page <= page_count:

            request_data_body['pager']['pageNum'] = page

            res = self._crawl(self.__QUERY_INDEX_ITEM_API, method='POST',
                              data=json.dumps(request_data_body),
                              headers=request_headers)
            res_text = res.text
            res_json = json.loads(res_text)

            res_code = res_json.get('code', None)
            if res_code is None or res_code != '200':
                page = page + 1
                continue

            res_page_count = res_json.get('size', None)
            if res_page_count is not None:
                page_count = res_page_count

            res_data = res_json.get('data', None)
            if res_data is None or len(res_data) <= 0:
                page = page + 1
                continue

            for idx_item in res_data:

                index_code = idx_item.get('indexCode', None)
                if index_code is None:
                    continue

                index_sname = idx_item.get('indexName', None)
                index_ename = idx_item.get('indexNameEn', None)
                con_num = idx_item.get('consNumber', None)
                online_date = idx_item.get('publishDate', None)
                class_region = idx_item.get('region', None)
                class_classify = idx_item.get('indexClassify', None)
                class_currency = idx_item.get('currency', None)

                idx_basic_info_list.append([
                    index_code, index_sname, index_ename,
                    int(con_num) if con_num is not None else None,
                    online_date,
                    class_region, class_classify, class_currency
                ])

            page = page + 1

        df_columns = ['index_code', 'index_sname', 'index_ename', 'con_num',
                      'online_date', 'class_region', 'class_classify',
                      'class_currency']
        idx_basic_info_df = pd.DataFrame(data=idx_basic_info_list,
                                            columns=df_columns)

        return idx_basic_info_df

    @cached(cache=TTLCache(maxsize=8192, ttl=600))
    def __get_idx_basic_info_detail_dict_by_id(self, idx_id):

        request_url = '%s/%s' % (self.__QUERY_INDEX_BASIC_API_TEMPLATE, idx_id)

        request_headers = {
            'Accept': 'application/json, text/plain, */*'
        }

        res = self._crawl(request_url, headers=request_headers)
        res_text = res.text
        res_json = json.loads(res_text)

        res_code = res_json.get('code', None)
        if res_code is None or res_code != '200':
            return None

        res_data = res_json.get('data', None)
        if res_data is None:
            return None

        return res_data

    def _get_idx_basic_point_by_id(self, idx_id):

        idx_basic_info_detail_dict = \
            self.__get_idx_basic_info_detail_dict_by_id(idx_id)

        return idx_basic_info_detail_dict.get('basicIndex', None)

    def _get_idx_basic_date_by_id(self, idx_id):

        idx_basic_info_detail_dict = \
            self.__get_idx_basic_info_detail_dict_by_id(idx_id)

        return idx_basic_info_detail_dict.get('basicDate', None)

    def _get_idx_cn_full_name_by_id(self, idx_id):

        idx_basic_info_detail_dict = \
            self.__get_idx_basic_info_detail_dict_by_id(idx_id)

        return idx_basic_info_detail_dict.get('indexFullNameCn', None)

    def _get_idx_en_full_name_by_id(self, idx_id):

        idx_basic_info_detail_dict = \
            self.__get_idx_basic_info_detail_dict_by_id(idx_id)

        return idx_basic_info_detail_dict.get('indexFullNameEn', None)

    def aindex_csi_stock_desc(self):

        idx_series_list = self.__get_idx_series_list()

        full_idx_df = pd.DataFrame()
        pbar = tqdm(total=len(idx_series_list), unit='page')

        for idx_serie_item in idx_series_list:

            tag_id = idx_serie_item.get('tagId', None)
            if tag_id is None:
                continue

            tag_name = idx_serie_item.get('tagName', '')
            tag_en_name = idx_serie_item.get('tagEname', '')

            idx_basic_info_df = self.__get_idx_basic_info_df_by_serie_id(tag_id)
            if idx_basic_info_df is None or len(idx_basic_info_df) <= 0:
                continue

            idx_basic_info_df['class_series'] = tag_name

            full_idx_df = full_idx_df.append(idx_basic_info_df,
                                             ignore_index=True)

            pbar.update(1)

        append_func = lambda x: pd.Series([
            self._get_idx_basic_point_by_id(x['index_code']),
            self._get_idx_basic_date_by_id(x['index_code']),
            self._get_idx_cn_full_name_by_id(x['index_code']),
            self._get_idx_en_full_name_by_id(x['index_code'])
        ])
        full_idx_df[['base_point', 'base_date',
                     'index_c_fullname', 'index_e_fullname']] = \
            full_idx_df.parallel_apply(append_func, axis=1)

        return full_idx_df

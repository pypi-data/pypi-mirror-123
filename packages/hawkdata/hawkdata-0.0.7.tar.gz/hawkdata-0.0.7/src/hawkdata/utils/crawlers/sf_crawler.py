# -*- coding:utf-8 -*-


import re, json, math
import pandas as pd, numpy as np

from tqdm import tqdm
from cachetools import cached, TTLCache

from hawkdata.utils.crawlers import WebCrawlerBase


class SfCrawler(WebCrawlerBase):

    JS_SDK_URL = 'http://finance.sina.com.cn/sinafinancesdk/js/sf_sdk.js'

    STOCK_BASE_URL = 'https://stock.finance.sina.com.cn'
    US_STOCK_API_BASE_URL = '%s/usstock/api/jsonp.php' % (STOCK_BASE_URL)
    US_STOCK_RT_LIST_API = \
        '%s/IO.XSRV2.CallbackList[]/US_CategoryService.getList' % (
            US_STOCK_API_BASE_URL)

    RE_STOCK_RT_LIST_JSON = re.compile('\(({.*})\);')

    __instance = None

    def __new__(self, *args, **kw):

        if self.__instance is None:
            self.__instance = object.__new__(self, *args, **kw)

        return self.__instance

    def __init__(self):

        pass

    @cached(cache=TTLCache(maxsize=1, ttl=300))
    def __get_stock_us_rt_df(self):

        STOCK_COUNT_PER_PAGE = 60

        request_params = {
            'num': STOCK_COUNT_PER_PAGE,
            'sort': '',
            'asc': 0,
            'market': '',
            'id': ''
        }

        page = 1
        page_count = 1
        result_list = []

        first_run = True
        pbar = tqdm(total=page_count, unit='part')

        while page <= page_count:

            request_params['page'] = page

            res = self._crawl(self.US_STOCK_RT_LIST_API, params=request_params)
            res_text = res.text

            rt_list_search_result = \
                self.RE_STOCK_RT_LIST_JSON.search(res_text)
            if rt_list_search_result is None:
                continue

            rt_list_json = json.loads(rt_list_search_result.group(1))

            stocks_data_list = rt_list_json.get('data', None)
            if stocks_data_list is None or len(stocks_data_list) <= 0:
                continue

            result_list = result_list + stocks_data_list

            if first_run is True:
                stock_count = rt_list_json['count']
                page_count = math.ceil(int(stock_count) / STOCK_COUNT_PER_PAGE)
                pbar.reset(total=page_count)
                first_run = False

            pbar.update(1)

            page = page + 1

        pbar.close()

        result_df = pd.DataFrame(result_list)

        return result_df

    @cached(cache=TTLCache(maxsize=1, ttl=3600))
    def stock_us_desc(self):

        stock_us_rt_df = self.__get_stock_us_rt_df()

        used_df = stock_us_rt_df[['symbol', 'name', 'cname', 'market']]

        return used_df

    def stock_us_price(self):

        stock_us_rt_df = self.__get_stock_us_rt_df()

        used_df = stock_us_rt_df[['symbol', 'price', 'diff', 'chg', 'open',
                                  'high', 'low', 'preclose', 'mktcap', 'pe']]

        return used_df

# -*- coding:utf-8 -*-


import pandas as pd

from hawkdata.utils.crawlers import EmCrawler


def mutual_fund_desc():

    RAW_DF_COLUMNS = ['fund_code', 'pinyin_short', 'fund_name', 'fund_type',
                      'pinyin_long']

    emc = EmCrawler()

    raw_json = emc.mutual_fund_desc()
    raw_df = pd.DataFrame(raw_json)
    raw_df.columns = RAW_DF_COLUMNS

    raw_df = raw_df.astype({
        'fund_code': 'string',
        'pinyin_short': 'string',
        'fund_name': 'string',
        'fund_type': 'string',
        'pinyin_long': 'string'
    })

    return raw_df.drop(['pinyin_short', 'pinyin_long'], axis=1)

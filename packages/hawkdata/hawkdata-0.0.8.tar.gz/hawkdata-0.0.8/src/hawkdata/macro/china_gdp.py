# -*- coding:utf-8 -*-

import pandas as pd

from hawkdata.utils.crawlers import CStatsCrawler


def macro_china_yearly_gdp():

    csc = CStatsCrawler()

    return csc.macro_china_yearly_gdp()

def macro_china_yearly_gdp_yoy():

    csc = CStatsCrawler()

    gdp_idx_df = csc.macro_china_yearly_gdp_idx()
    gdp_yoy_df = gdp_idx_df.rename(columns={
        'gdp_idx': 'gdp_yoy'
    })
    gdp_yoy_df['gdp_yoy'] = gdp_yoy_df['gdp_yoy'].apply(lambda x: (x/100)-1)

    return gdp_yoy_df

def macro_china_yearly_gdp_index():

    csc = CStatsCrawler()

    return csc.macro_china_yearly_gdp_index()

def macro_china_quarterly_gdp():

    csc = CStatsCrawler()

    return csc.macro_china_quarterly_gdp()

def macro_china_quarterly_gdp_yoy():

    csc = CStatsCrawler()
    gdp_idx_df = csc.macro_china_quarterly_gdp_idx()
    gdp_yoy_df = gdp_idx_df.rename(columns={
        'gdp_idx': 'gdp_yoy'
    })
    gdp_yoy_df['gdp_yoy'] = gdp_yoy_df['gdp_yoy'].apply(lambda x: (x/100)-1)

    return gdp_yoy_df

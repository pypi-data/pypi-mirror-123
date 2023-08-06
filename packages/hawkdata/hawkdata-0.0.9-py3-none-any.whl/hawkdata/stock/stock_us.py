# -*- coding:utf-8 -*-


from hawkdata.utils.crawlers import SfCrawler, EmCrawler


def stock_us_desc():

    sfc = SfCrawler()

    stock_desc_df = sfc.stock_us_desc()
    stock_desc_df = stock_desc_df.rename(columns={
        'symbol': 'stock_code',
        'cname': 'chinese_name',
        'market': 'exchange_market'
    })

    return stock_desc_df

def stock_us_price():

    sfc = SfCrawler()

    stock_price_df = sfc.stock_us_price()
    stock_price_df = stock_price_df.rename(columns={
        'symbol': 'stock_code',
        'price': 'latest',
        'diff': 'change',
        'change': 'pct_change',
        'preclose': 'pre_close',
        'mktcap': 'mv'
    })

    return stock_price_df

def stock_us_price_hist(stock_code,
                        start_date=None, end_date=None,
                        adj_mode=''):

    emc = EmCrawler()

    stock_price_hist_df = emc.stock_us_price_hist(stock_code,
                                                  start_date, end_date,
                                                  adj_mode)

    return stock_price_hist_df

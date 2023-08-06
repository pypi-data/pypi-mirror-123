# -*- coding:utf-8 -*-


import time
import pandas as pd
import numpy as np

from hawkdata.utils.crawlers import EmCrawler


def mutual_fund_nav(fund_code, adj=False):

    emc = EmCrawler()

    # 获取单位净值和累计净值的 List
    unit_nav_list, acc_nav_list, is_money_fund = \
        emc.mutual_fund_unit_and_acc_nav(fund_code)

    # 如果是货币基金，则通过该逻辑单独处理
    if is_money_fund is True:

        nav_df = pd.DataFrame(unit_nav_list)

        columns_list = ['nav_date', 'unit_nav', 'unit_yield', 'yearly_roe']
        if adj is True:
            columns_list = columns_list + ['adj_nav']

        return nav_df[columns_list]

    # 通过净值 List 生成对应的 DataFrame，便于根据 nav_date 进行合并
    unit_nav_df = pd.DataFrame(unit_nav_list)
    acc_nav_df = pd.DataFrame(acc_nav_list)

    # 通过 nav_date 将单位净值和累计净值信息合入一个 DataFrame
    integrated_nav_df = \
        unit_nav_df.join(acc_nav_df.set_index('nav_date'),
                         how='outer',
                         on='nav_date',
                         sort=True)

    # 如果参数指定不计算复权净值，则直接返回基本净值信息
    if adj is False:
        integrated_nav_df = integrated_nav_df[[
            'nav_date', 'unit_nav', 'acc_nav']]
        return integrated_nav_df

    dividend_df, split_df = emc.mutual_fund_dividend_and_split(fund_code)

    # 如果该基金历史分红信息不为空，则对其进行关联，用于计算复权净值
    if dividend_df is not None:
        integrated_nav_df = integrated_nav_df.merge(dividend_df, how='outer',
                                                    left_on='nav_date',
                                                    right_on='ex_date',
                                                    sort=True)
        integrated_nav_df = integrated_nav_df.drop(['eqy_record_date',
                                                    'pay_date'],
                                                   axis=1)
        integrated_nav_df = integrated_nav_df.astype({
            'dvd_per_sh': 'float64'
        })

    # 如果该基金历史拆分信息不为空，则对其进行关联，用于计算复权净值
    if split_df is not None:
        integrated_nav_df = integrated_nav_df.merge(split_df, how='outer',
                                                    left_on='nav_date',
                                                    right_on='split_date',
                                                    sort=True)
        integrated_nav_df = integrated_nav_df.drop(['split_type'],
                                                   axis=1)
        integrated_nav_df = integrated_nav_df.astype({
            'split_inc': 'float64'
        })

    # 处理因 outer join 分红送配信息导致的部分主要列值缺失问题；
    for index, row in integrated_nav_df.iterrows():

        # 对于第一行，即便有所缺失，也没有信息可参考处理，故直接忽略
        if 0 == index:
            continue

        # 补全因 outer join 而缺失的 nav_date
        if pd.isnull(row['nav_date']):

            if 'ex_date' in integrated_nav_df.columns:
                integrated_nav_df.loc[index, 'nav_date'] = \
                    integrated_nav_df['ex_date'].iloc[index]
                integrated_nav_df = integrated_nav_df.drop(['ex_date'], axis=1)
            elif 'split_date' in integrated_nav_df.columns:
                integrated_nav_df.loc[index, 'nav_date'] = \
                    integrated_nav_df['split_date'].iloc[index]
                integrated_nav_df = integrated_nav_df.drop(['split_date'],
                                                           axis=1)
            else:
                continue

        # 补全因 outer join 而缺失的 unit_nav
        if pd.isnull(row['unit_nav']):
            integrated_nav_df.loc[index, 'unit_nav'] = \
                integrated_nav_df['unit_nav'].iloc[index-1]

        # 补全因 outer join 而缺失的 acc_nav
        if pd.isnull(row['acc_nav']):
            integrated_nav_df.loc[index, 'acc_nav'] = \
                integrated_nav_df['acc_nav'].iloc[index-1]

    integrated_nav_df['adj_nav'] = np.nan
    integrated_nav_df['adj_nav_return'] = np.nan
    integrated_nav_df['adj_factor'] = np.nan

    # 计算复权净值日增长率和复权净值
    for index, row in integrated_nav_df.iterrows():

        if 0 == index:
            integrated_nav_df.loc[0, 'adj_nav'] = \
                integrated_nav_df['unit_nav'].iloc[0]
            integrated_nav_df.loc[0, 'adj_factor'] = 1
            continue

        # 设置分红参数
        if 'dvd_per_sh' not in integrated_nav_df.columns or \
                pd.isnull(row['dvd_per_sh']):
            dvd_per_sh = 0
        else:
            dvd_per_sh = integrated_nav_df['dvd_per_sh'].iloc[index]

        # 设置拆分参数
        if 'split_inc' not in integrated_nav_df.columns or \
                pd.isnull(row['split_inc']):
            split_inc = 1
        else:
            split_inc = integrated_nav_df['split_inc'].iloc[index]

        prev_adj_factor = integrated_nav_df['adj_factor'].iloc[index-1]
        prev_unit_nav = integrated_nav_df['unit_nav'].iloc[index-1]
        prev_adj_nav = integrated_nav_df['adj_nav'].iloc[index-1]
        curr_unit_nav = integrated_nav_df['unit_nav'].iloc[index]

        prev_excluded_nav = prev_unit_nav - dvd_per_sh

        curr_adj_factor = \
            prev_adj_factor * prev_unit_nav / prev_excluded_nav * split_inc
        curr_adj_nav = curr_unit_nav * curr_adj_factor
        curr_nav_return = (curr_adj_nav - prev_adj_nav) / prev_adj_nav

        integrated_nav_df.loc[index, 'adj_nav'] = curr_adj_nav
        integrated_nav_df.loc[index, 'adj_factor'] = curr_adj_factor
        integrated_nav_df.loc[index, 'adj_nav_return'] = curr_nav_return

    integrated_nav_df = integrated_nav_df[[
        'nav_date', 'unit_nav', 'acc_nav', 'adj_nav', 'adj_nav_return']]

    return integrated_nav_df

def mutual_fund_dividend_and_split(fund_code):

    emc = EmCrawler()

    return emc.mutual_fund_dividend_and_split(fund_code)

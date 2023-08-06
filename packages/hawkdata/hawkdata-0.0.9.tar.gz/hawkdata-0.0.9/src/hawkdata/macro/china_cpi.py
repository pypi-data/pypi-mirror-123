# -*- coding:utf-8 -*-


from hawkdata.utils.crawlers import CStatsCrawler


def macro_china_yearly_cpi_yoy():

    csc = CStatsCrawler()

    cpi_idx_df = csc.macro_china_yearly_cpi_idx()
    cpi_yoy_df = cpi_idx_df.rename(columns={
        'cpi_idx': 'cpi_yoy'
    })
    cpi_yoy_df['cpi_yoy'] = cpi_yoy_df['cpi_yoy'].apply(lambda x: (x/100)-1)

    return cpi_yoy_df

def macro_china_yearly_cpi_index():

    csc = CStatsCrawler()

    return csc.macro_china_yearly_cpi_fixed_base_idx()

def macro_china_monthly_cpi_yoy():

    csc = CStatsCrawler()

    cpi_idx_monthly_df = csc.macro_china_monthy_cpi_idx()

    cpi_yoy_monthly_df = cpi_idx_monthly_df.rename(columns={
        'cpi_idx': 'cpi_yoy'
    })
    cpi_yoy_monthly_df['cpi_yoy'] = \
        cpi_yoy_monthly_df['cpi_yoy'].apply(lambda x: (x/100)-1)

    return cpi_yoy_monthly_df

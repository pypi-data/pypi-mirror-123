# -*- coding:utf-8 -*-

from datetime import datetime

from hawkdata.utils.crawlers import CbCrawler
from hawkdata.utils.datetimex import datetimex as dtx


def cbond_curve_yield(ids, start_date=None, end_date=None):

    DATE_FORMAT = '%Y-%m-%d'

    DEFAULT_RECENT_DAYS = 30

    cbc = CbCrawler()

    if end_date is None:
        end_date = dtx.get_yesterday_date()
    else:
        end_date = datetime.strptime(end_date, DATE_FORMAT).date()

    if start_date is None:
        start_date = dtx.get_date_after_days(end_date, 1-DEFAULT_RECENT_DAYS)
    else:
        start_date = datetime.strptime(start_date, DATE_FORMAT).date()

    id_list = ids.split(',')
    date_list = dtx.get_date_list_between(start_date, end_date)

    curve_df = cbc.cbond_curve_yield(id_list, date_list)

    return curve_df

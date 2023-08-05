# -*- coding:utf-8 -*-

from datetime import datetime, timedelta

def now():

    return datetime.now()

def get_current_date():

    return datetime.now().date()

def get_yesterday_date():

    current_date = get_current_date()
    yesterday_date = get_date_after_days(current_date, -1)

    return yesterday_date

def get_date_after_days(dt, days):

    return dt + timedelta(days=days)

def get_date_list_between(start_date, end_date):

    date_list = []
    anchor = start_date
    while anchor <= end_date:
        date_list.append(anchor)
        anchor = get_date_after_days(anchor, 1)

    return date_list

def get_recent_n_days_list(n, current_date=None):

    if current_date is None:
        current_date = get_current_date()

    prev_date = current_date + timedelta(days=1-n)

    return get_date_list_between(prev_date, current_date)

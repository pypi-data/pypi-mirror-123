# -*- coding:utf-8 -*-


from hawkdata.utils.crawlers import CsIdxCrawler, CnIdxCrawler

def aindex_csi_stock_desc():

    csic = CsIdxCrawler()

    return csic.aindex_csi_stock_desc()

def aindex_cni_stock_desc():

    cnic = CnIdxCrawler()

    return cnic.aindex_cni_stock_desc()

def aindex_price_hist():

    pass

def aindex_members():

    pass

def aindex_members_hist():

    pass

# -*- coding:utf-8 -*-


def convert_list_to_string_without_quota(src_list, delimeter):

    return delimeter.join(str(x) for x in src_list)

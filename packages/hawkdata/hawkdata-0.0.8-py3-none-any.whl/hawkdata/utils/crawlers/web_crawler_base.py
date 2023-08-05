# -*- coding:utf-8 -*-


import requests, socket, struct

from retrying import retry
from random import seed, randint
from urllib.parse import urlparse
from retrying import retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from hawkdata.utils.crawlers import USER_AGENT_LIST, REFERER_LIST

class WebCrawlerBase:

    def __init__(self, proxyPool=None):

        pass

    def _get_random_user_agent(self):

        seed()
        idx = randint(0, len(USER_AGENT_LIST)-1)

        return USER_AGENT_LIST[idx]

    def _get_random_referer(self):

        seed()
        idx = randint(0, len(REFERER_LIST)-1)

        return REFERER_LIST[idx]

    def _get_random_ipv4_address(self):

        seed()
        ipv4Addr = socket.inet_ntoa(
            struct.pack('>I', randint(1, 0xffffffff)))

        return ipv4Addr

    def _add_general_header_fields(self, headers):

        if 'User-Agent' not in headers:
            headers['User-Agent'] = self._get_random_user_agent()

        if 'DNT' not in headers:
            headers['DNT'] = '1'

        if 'Referer' not in headers:
            headers['Referer'] = self._get_random_referer()

        if 'Accept' not in headers:
            headers['Accept'] = '*/*'

        if 'Accept-Encoding' not in headers:
            headers['Accept-Encoding'] = 'gzip, deflate, br'

        if 'Accept-Language' not in headers:
            headers['Accept-Language'] = 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'

        if 'sec-ch-ua-mobile' not in headers:
            headers['sec-ch-ua-mobile'] = '?0'

        return headers

    def _get_hostname_from_url(self, url):

        parsedUrl = urlparse(url)
        host = '{uri.netloc}'.format(uri=parsedUrl)

        return host

    @retry(stop_max_attempt_number=3,
           wait_random_min=1000,
           wait_random_max=3000)
    def _crawl(self, url, method='GET',
              headers={}, params={}, data={}, timeout=5, ssl_verify=True,
               cookies_dict={}):

        m = method.lower()
        if m == 'get':
            func_request = requests.get
        elif m == 'post':
            func_request = requests.post
        elif m == 'put':
            func_request = requests.put
        elif m == 'head':
            func_request = requests.head
        else:
            raise Exception('unsupported method: [%s]' % method)

        headers = self._add_general_header_fields(headers)
        headers['X-Forwarded-For'] = self._get_random_ipv4_address()

        # Disable Insecure HTTPS Warning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        resp = func_request(url, headers=headers, params=params, data=data,
                            timeout=timeout, verify=ssl_verify)

        return resp

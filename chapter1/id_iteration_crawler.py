import urllib.request
from urllib.error import URLError,HTTPError,ContentTooShortError
import re
import itertools


def download(url,num_retries=2,user_agent='lucas',charset='utf-8'):
    print('Downloading:',url)
    request = urllib.request.Request(url)
    request.add_header('User-agent',user_agent)
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs =charset
        html = resp.read().decode(cs)
    except (URLError,HTTPError,ContentTooShortError) as e:
        print('Download error:',e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500 <= e.code <600:
                return download(url,num_retries-1)
    return html

def crawl_site(url,max_errors=5):
    num_error=0
    for page in itertools.count(1):
        pg_url='{}{}'.format(url,page)
        print(page,pg_url)
        html=download(pg_url)
        if html is None:
            num_error +=1
            if num_error == max_errors:
                break;
        else:
            num_error = 0

crawl_site('http://example.webscraping.com/view/-')

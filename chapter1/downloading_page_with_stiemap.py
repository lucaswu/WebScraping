
import urllib.request
from urllib.error import URLError,HTTPError,ContentTooShortError
import re


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

def crawl_sitemap(url):
    #sownload the sitemap file
    sitemap=download(url)
    #extract the sitemap links
    links =re.findall('<loc>(.*?)</loc>',sitemap)
    #download each link
    for link in links:
        html = download(link)

crawl_sitemap('http://www.lofter.com/sitemap.xml')

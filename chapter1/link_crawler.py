import urllib.request
from urllib.error import URLError,HTTPError,ContentTooShortError
import re
import itertools
from urllib.parse import   urljoin


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

def get_links(html):
    " Return a list of links from html "
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

def link_crawler(start_url,link_regex):
    """
    crawl from the given start URL fllowing links matched by link_regex
    """
    crawl_queue=[start_url]
    seen = set(crawl_queue)

    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        if html is None:
            continue
        for link in get_links(html):
            print(link,'==',link_regex)
            #if re.match(link_regex, link):
            if re.match(link,link_regex):
                print('ok')
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)
            else:
                print('error!')


link_crawler('http://example.webscraping.com', '/(index|view)/')

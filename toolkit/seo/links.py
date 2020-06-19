
from bs4 import BeautifulSoup
from toolkit.lib.http_tools import request_parse, request_status_code
import urllib

def find_all_links(url):
    list_urls = {}
    list_visited = []
    soup = request_parse(url, timeout=1)
    for link in soup.findAll('a'):
        
        url = urllib.parse.urljoin(url, link.get('href'))
        if url not in list_visited:
            status_code = request_status_code(url, timeout=1)
            if status_code not in list_urls:
                list_urls[status_code] = []
            if url not in list_urls[status_code]:
                list_urls[status_code].append(url)
                list_visited.append(url)
    return list_urls


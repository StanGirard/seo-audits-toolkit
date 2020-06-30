from toolkit.lib.http_tools import request_parse, request_status_code
import urllib

def find_all_links(url):
    list_urls = {}
    list_visited = []
    soup = request_parse(url, timeout=1)
    for link in soup.findAll('a'):
        url2 = urllib.parse.urljoin(url, link.get('href'))
        if url2 not in list_visited:
            status_code = request_status_code(url, timeout=1)
            if status_code not in list_urls:
                list_urls[status_code] = []
            if url2 not in list_urls[status_code]:
                list_urls[status_code].append(url2)
                list_visited.append(url2)
    return list_urls



from bs4 import BeautifulSoup
from toolkit.lib.http_tools import request_parse
import urllib

def find_all_images(url):
    list_images = {"images":[], "summary":{"missing_title": 0, "missing_alt": 0}}
    list_urls =  []
    soup = request_parse(url, timeout=1)
    images = soup.findAll('img')
    for image in images:
        url = urllib.parse.urljoin(url,image['src'])
        alt = None
        title = None
        if "alt" in image:
            alt  = image['alt']
        else:
            list_images["summary"]["missing_alt"] += 1
        if "title" in image:
            title = image["title"]
        else:
            list_images["summary"]["missing_title"] += 1
        if url not in list_urls:
            list_images["images"].append({"url": url, "alt": alt, "title": title})
            list_urls.append(url)
    return list_images
    

    

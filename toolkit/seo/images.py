
from bs4 import BeautifulSoup
from toolkit.lib.http_tools import request_parse
import urllib

def find_all_images(url):
    list_images = {"images":[]}
    list_urls =  []
    soup = request_parse(url, timeout=1)
    images = soup.findAll('img')
    for image in images:
        url = urllib.parse.urljoin(url,image['src'])
        alt = image['alt']
        if url not in list_urls:
            list_images["images"].append({"url": url, "alt": alt})
            list_urls.append(url)
    return list_images
    

    

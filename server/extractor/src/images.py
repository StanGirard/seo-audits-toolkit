from extractor.lib.http_tools import request_parse
import urllib

def find_all_images(url):
    list_images = {"images":[], "summary":{"missing_title": 0, "missing_alt": 0,"duplicates":0, "total": 0}}
    list_urls =  []
    soup = request_parse(url, timeout=1)
    images = soup.findAll('img')
    for image in images:
        url_img = None
        
        if image.has_attr('src'):
            
            url_img = urllib.parse.urljoin(url,image['src'])
        elif image.has_attr('data-src'):
            url_img = urllib.parse.urljoin(url,image['data-src'])
        elif image.has_attr('src-set'):
            url_img = urllib.parse.urljoin(url,image['src-set'])
        alt = image.get("alt")
        title = image.get("title")
        list_images["summary"]["total"] += 1
        if url_img:
            if not alt:
                list_images["summary"]["missing_alt"] += 1
            if not title:
                list_images["summary"]["missing_title"] += 1
            if url_img not in list_urls:
                list_images["images"].append({"url": url_img, "alt": alt, "title": title})
                list_urls.append(url_img)
            else:
                list_images["summary"]["duplicates"] +=1
    return list_images
    

    

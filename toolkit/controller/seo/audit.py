import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import timeit
import json

total_urls_visited = 0 
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url, internal_urls, external_urls):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                external_urls.add(href)
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url,internal_urls, external_urls, max_urls=50):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url, internal_urls, external_urls)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link,internal_urls, external_urls, max_urls=max_urls)
    return internal_urls, external_urls


def get_all_links_website(url, max_urls=50):

    internal_urls = set()
    external_urls = set()
    start = timeit.default_timer()

    crawl(url,internal_urls, external_urls, max_urls=max_urls)
    stop = timeit.default_timer()

    domain_name = urlparse(url).netloc

    results = {"internal_urls": {
        "total": len(internal_urls),
        "results": list(internal_urls)
        }, "external_urls" : {
            "total": len(external_urls),
            "results": list(external_urls)
        },
        "total": len(external_urls) + len(internal_urls),
        "domain_name": domain_name,
        "time_crawl": stop - start,
        "page_visited": total_urls_visited
    } 
    return results
    


if __name__ == "__main__":
    print(get_all_links_website("https://primates.dev", max_urls=50))
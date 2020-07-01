from urllib.parse import urlparse
from toolkit.lib.http_tools import request_page
from bs4 import BeautifulSoup, Doctype
import requests
import pandas as pd
import hashlib


class AuditWebsite():
    def __init__(self, url):
        parsed_url = urlparse(url)
        self.domain = parsed_url.netloc
        self.scheme = parsed_url.scheme
        self.path = parsed_url.path
        self.sitemap = []
        self.robots = False
        self.populate_request()
        self.robots_finder()
        self.populate_urls()
        self.soup = BeautifulSoup(self.request.content, features="lxml")
        self.populate_doctype()
    
    def populate_request(self):
        self.request = request_page(self.generate_url())
        self.status_code = self.request.status_code

    def robots_finder(self):
        request = request_page(self.generate_url() + "/robots.txt")
        if request.status_code == 200:
            self.robots_present = True
            self.find_sitemap(request.text)

    def find_sitemap(self, robots):
        self.sitemap = []
        for line in robots.split("\n"):
            line = line.lower()
            line = line.split(" ")
            if line[0] == "sitemap:":
                self.sitemap.append(line[1])
            if line[0] == "sitemaps:":
                self.sitemap.append(line[1])
        
    def populate_urls(self):
        list_urls = []
        self.urls = []
        
        if len(self.sitemap) > 0:
            for i in self.sitemap:
                sitemap_urls = parse_sitemap(i)
                for url in sitemap_urls:
                    if url not in list_urls:
                        list_urls.append(url)
            self.urls = list_urls
    
    def populate_doctype(self):
        items = [item for item in self.soup.contents if isinstance(item, Doctype)]
        self.doctype = items[0] if items else None

    def generate_url(self):
        return self.scheme + "://" + self.domain





def parse_sitemap( url):
    resp = requests.get(url)
    # we didn't get a valid response, bail
    if (200 != resp.status_code):
        return False

    # BeautifulSoup to parse the document
    soup = BeautifulSoup(resp.content, "xml")

    # find all the <url> tags in the document
    urls = soup.findAll('url')
    sitemaps = soup.findAll('sitemap')
    panda_out_total = []


    if not urls and not sitemaps:
        return False

    # Recursive call to the the function if sitemap contains sitemaps
    if sitemaps:
        for u in sitemaps:
            test = u.find('loc').string
            panda_recursive = parse_sitemap(test)
            panda_out_total += panda_recursive

    # storage for later...
    out = []

    # Extract the keys we want
    for u in urls:
        loc = None
        loc = u.find("loc")
        if not loc:
            loc = "None"
        else:
            loc = loc.string
        out.append(loc)

    #returns the dataframe
    return  panda_out_total + out
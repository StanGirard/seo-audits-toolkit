from urllib.parse import urlparse
from toolkit.lib.http_tools import request_page
from bs4 import BeautifulSoup, Doctype
import requests
import pandas as pd
import hashlib
from .lib import generate_audit_json, generate_result_bool, generate_result_int

class AuditWebsite():
    def __init__(self, url):
        parsed_url = urlparse(url)
        self.domain = parsed_url.netloc
        self.scheme = parsed_url.scheme
        self.path = parsed_url.path
        self.audit_results = generate_audit_json()
        self.sitemap = []
        self.robots = False
        self.cms = None
        self.populate_request()
        self.robots_finder()
        self.populate_urls()
        self.soup = BeautifulSoup(self.request.content, features="html.parser")
        self.populate_doctype()
        self.is_https()
        self.get_cms()
        self.find_google_analytics()
        self.meta_description_title()
        self.deprecated_html_tags()

    def populate_request(self):
        self.request = request_page(self.generate_url())
        self.status_code = self.request.status_code

    def robots_finder(self):
        request = request_page(self.generate_url() + "/robots.txt")
        if request.status_code == 200:
            self.robots = True
            robot_answer = self.audit_results["common_seo_issues"]["audits"]["robots"]
            robot_answer["score"] = True
            robot_answer["result"] = self.generate_url() + "/robots.txt"
            robot_answer["success"] = robot_answer["success"].replace("{value}",self.generate_url() + "/robots.txt")
            self.audit_results["common_seo_issues"]["audits"]["robots"] = robot_answer
            self.find_sitemap(request.text)

    def find_sitemap(self, robots):
        self.sitemap = []
        for line in robots.split("\n"):
            line = line.lower()
            line = line.split(" ")
            if line[0] == "sitemap:":
                self.sitemap.append(line[1].replace('\r', ''))
            if line[0] == "sitemaps:":
                self.sitemap.append(line[1].replace('\r', ''))
        if len(self.sitemap):
            sitemap_save = self.audit_results["common_seo_issues"]["audits"]["sitemap"]
            sitemap_save["score"] = True
            sitemap_save["result"] = self.sitemap
            sitemap_save["success"] = sitemap_save["success"].replace("{value}", self.sitemap[0])
            self.audit_results["common_seo_issues"]["audits"]["sitemap"] = sitemap_save


    def populate_urls(self):
        list_urls = []
        self.urls = []

        if len(self.sitemap) > 0:
            for i in self.sitemap:
                sitemap_urls = self.parse_sitemap(i)
                if sitemap_urls:
                    for url in sitemap_urls:
                        if url not in list_urls:
                            list_urls.append(url)
            self.urls = list_urls

    def populate_doctype(self):
        items = [
            item for item in self.soup.contents if isinstance(item, Doctype)]
        self.doctype = items[0] if items else None
        if self.doctype:
            generate_result_bool(self.audit_results, "common_seo_issues", "doctype", True, self.doctype)
        else:
            generate_result_bool(self.audit_results, "common_seo_issues", "doctype", False)

    def is_https(self):
        https_save = self.audit_results["common_seo_issues"]["audits"]["https"]
        if request_page("https://" + self.domain).status_code == 200:
            self.https = True
            https_save["score"] = True
        else:
            self.https = False
            https_save["score"] = False
        self.audit_results["common_seo_issues"]["audits"]["https"] = https_save

    def generate_url(self):
        return self.scheme + "://" + self.domain

    def get_cms(self):
        metatags = self.soup.find_all('meta', attrs={'name': 'generator'})
        if metatags:
            self.cms = metatags[0]["content"]

    
    
    def find_google_analytics(self):
        scripts = self.soup.find_all('script')
        self.google_analytics = False
        ga_save = self.audit_results["common_seo_issues"]["audits"]["google_analytics"]
        ga_save["score"] = False
        for i in scripts:
            if "googletagmanager" in str(i) or "google-analytics" in str(i):
                self.google_analytics = True
                ga_save["score"] = True
        self.audit_results["common_seo_issues"]["audits"]["google_analytics"] = ga_save
    
    def meta_description_title(self):
        title = self.soup.find('title')
        if len(title.text) > 0 and len(title.text) < 70:
            generate_result_int(self.audit_results, "common_seo_issues", "meta_title", True, len(title.text))
        else:
            generate_result_int(self.audit_results, "common_seo_issues", "meta_title", False, len(title.text))
        
        description = self.soup.find('meta', attrs={'name': 'description'})
        if len(description["content"]) > 0 and len(description["content"]) < 160:
            generate_result_int(self.audit_results, "common_seo_issues", "meta_description", True, len(description["content"]))
        else:
            generate_result_int(self.audit_results, "common_seo_issues", "meta_description", False, len(description["content"]))

    def deprecated_html_tags(self):
        deprecated = ["acronym", "applet","basefont", "big","center", "dir", "font", "frame", "frameset", "noframes", "strike", "tt"]
        deprecated_found = []
        for tag in deprecated:
            tags = self.soup.find(tag)
            if tags:
                deprecated_found.append(tag)
        if len(deprecated_found) == 0:
            generate_result_bool(self.audit_results, "common_seo_issues", "deprecated_tag", True)
        else:  
            generate_result_bool(self.audit_results, "common_seo_issues", "deprecated_tag", False, str(deprecated_found))


    def parse_sitemap(self, url):
        resp = requests.get(url)
        # we didn't get a valid response, bail
        if (200 != resp.status_code):
            return

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
                if test not in self.sitemap:
                    self.sitemap.append(test)
                panda_recursive = self.parse_sitemap(test)
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

        # returns the dataframe
        return panda_out_total + out

    

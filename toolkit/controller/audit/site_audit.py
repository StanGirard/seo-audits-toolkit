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
        self.audit_results = self.generate_audit_json()
        self.sitemap = []
        self.robots = False
        self.cms = None
        self.populate_request()
        self.robots_finder()
        self.populate_urls()
        self.soup = BeautifulSoup(self.request.content, features="lxml")
        self.populate_doctype()
        self.is_https()
        self.get_cms()

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

    def generate(self):
        result = {"domain": self.domain, "scheme": self.scheme, "path": self.path, "sitemap": self.sitemap,
                  "robots": self.robots, "doctype": self.doctype, "cms": self.cms, "https": self.https}
        return result

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
    
    def generate_audit_json(self):
        audit_results = {
            "common_seo_issues":
            {
                "description": "Common Errors",
                "title": "Common SEO Isssues",
                "audits":
                {
                    "meta_title":
                        {
                            "title": "Meta Title Test",
                            "description": "The meta title of your page has a length of {value} characters. Most search engines will truncate meta titles to 70 characters.",
                            "result": None,
                            "score": None,
                            "score_type": "int"
                        },
                    "meta_description":
                        {
                            "title": "Meta Description Test",
                            "description": "The meta description of your page has a length of {value} characters. Most search engines will truncate meta descriptions to 160 characters.",
                            "result": None,
                            "score": None,
                            "score_type": "int"
                        },
                    "robots":
                        {
                            "title": "Robots.txt Test",
                            "success": "Congratulations! Your site uses a 'robots.txt' file: <a href='{value}'>{value}</a>",
                            "error": "Your site doesn't have a 'robots.txt' file",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        },
                    "sitemap":
                        {
                            "title": "Sitemap Test",
                            "success": "Congratulations! Your site has a sitemap: <a href='{value}'>{value}</a>",
                            "error": "Your site doesn't have a sitemap",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        },
                    "https":
                        {
                            "title": "Https Test",
                            "success": "Congratulations! Your website uses https",
                            "error": "Your site doesn't use https. Your ranking will be impacted",
                            "result": None,
                            "score": None,
                            "score_type": "bool"
                        }
                }
            }

        }
        return audit_results

from urllib.parse import urlparse
from toolkit.lib.http_tools import request_page
from bs4 import BeautifulSoup

class AuditPage():
    def __init__(self, url):
        parsed_url = urlparse(url)
        self.domain = parsed_url.netloc
        self.scheme = parsed_url.scheme
        self.path = parsed_url.path
        self.request = request_page(self.generate_url())
        self.status_code = self.request.status_code
        self.headers = self.request.headers
        self.soup = BeautifulSoup(self.request.content, 'html.parser')
        
        
    def __str__(self):
        a  = "--------------------\n" 
        a += "Domain: " + self.domain + "\n"
        a += "Scheme: " + self.scheme + "\n"
        a += "Path: " + self.path + "\n"
        a += "Status Code: " + str(self.status_code) + "\n"
        a += "Headers: " + str([x for x in self.headers]) + "\n"
        return a




    def generate_url(self):
        return self.scheme + "://" + self.domain + "/" + self.path





        
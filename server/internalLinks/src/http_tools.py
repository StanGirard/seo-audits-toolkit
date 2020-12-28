import requests
from bs4 import BeautifulSoup


def request_status_code(url, timeout = 1):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code
    except:
        return 500

def request_page(url, timeout = 1):
    try:
        response = requests.get(url, timeout=timeout)
        return response
    except:
        return None


def request_parse(url, timeout = 1):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.content, "lxml")
        return soup
    except:
        return


def check_internal(website, url):
    if website not in url:
        return False
    return True
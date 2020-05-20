import requests
import re
import math
from bs4 import BeautifulSoup
import urllib.parse
import networkx as nx

import matplotlib.pyplot as plt
import numpy as np



def request_status_code(url):
    try :
        response = requests.get(url)
        return response.status_code
    except :
        return 500
    

def request_parse(url):
    try :
        response = requests.get(url)
        if response.status_code != 200:
            return 
        soup = BeautifulSoup(response.content, "lxml")
        return soup
    except :
        return 

def check_internal(website, url):
    if website not in url:
        return False
    return True

def find_all_headings(soup):
    headings = {"h1":{"count": 0, "header" :[]}, "h2":{"count": 0, "header" :[]},
                "h3": {"count": 0, "header" :[]}, "h4":{"count": 0, "header" :[]}, 
                "h5":{"count": 0, "header" :[]}, "h6":{"count": 0, "header" :[]}}
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        headings[heading.name]["header"].append(heading.text.strip())
        headings[heading.name]["count"] += 1
    return headings

def print_all_headers(headers_list):
    for key in headers_list:
        for i in headers_list[key]["header"]:
            print(key + " " + i)

def print_specific_header(headers_list, header):
    for i in headers_list[header]["header"]:
            print(header + " " + i)
        
def print_all_headers_count(headers_list):
    for key in headers_list:
        print("Number of " + key + " : " + str(headers_list[key]["count"]))

def print_specific_header_count(headers_list, header):
    print("Number of " + header + " : " + str(headers_list[header]["count"]))

def find_all_urls_single_page(source,soup):
    list_urls = {source:{"urls":{}, "count": 0, "broken": 0}}
    for link in soup.findAll('a'):
        url = urllib.parse.urljoin(source, link.get('href'))
        if url not in list_urls[source]['urls']:
            status_code = request_status_code(url)
            if status_code == 200:
                list_urls[source]["urls"][url] = {"status": 200, "count": 1}
            else:
                list_urls[source]["urls"][url] = {"status": status_code, "count": 1} 
                list_urls[source]["broken"] += 1
            list_urls[source]["count"] += 1
        else:
            list_urls[source]["urls"][url]["count"] += 1
            
    return list_urls

def extract_path(url):
    try:
        path = urllib.parse.urlparse(url).path
        if path == "":
            return "/"
        return urllib.parse.urlparse(url).path
    except:
        return "/"

def add_edge(list_urls, url, domain):
    if domain not in url:
        print(url + " not in domain")
        return
    
    if extract_path(url) not in list_urls and domain in url and  (url.startswith("https://" + domain)  or url.startswith("http://" + domain)):
        list_urls[extract_path(url)] = []
        print("Requesting " + url)
        soup = request_parse(url)
        if soup:
            for link in soup.find_all('a'):
                url_joined = urllib.parse.urljoin(url, link.get('href'))

                if url_joined.startswith("https://" + domain) or url_joined.startswith("http://" + domain):
                    if url_joined not in list_urls[extract_path(url)] :
                        #print("Going down in " + url_joined)
                        list_urls[extract_path(url)].append(extract_path(url_joined))
                        #print(list_urls[extract_path(url)])
                        
                        add_edge(list_urls, url_joined, domain)
            return list_urls
        
    return list_urls
    
    
        


def main(website, domain):
    #soup = request_parse(website)
    #headings = find_all_headings(soup)
    print("Adding Edges")
    urls = add_edge({}, website, domain)
    
    g = nx.Graph(urls)
    

    #nx.draw(g, with_labels=True)
    #nx.draw(g)
    d = dict(g.degree)
    #nx.draw(g, nodelist=d.keys(), node_size=[v * 20 for v in d.values()], with_labels=True,font_size=4)
    #(g, with_labels=True, font_size=4, nodelist=d.keys(), node_size=[20 * pow(v,1.2) for v in d.values()])
    #node_size=[20 * pow(v,1.01) for v in d.values()]
    
    
    #nx.draw(g, pos=pos, nodelist=d.keys(), node_size=[v * 20 for v in d.values()], font_size=4)

    #pos = nx.kamada_kawai_layout(g)
    size = g.number_of_nodes()
    print("SIZE")
    print(size)
    plt.figure(num=None, figsize=(30 * math.ceil(math.sqrt(size) / 8), 20 * math.ceil(math.sqrt(size)/ 8 )), dpi=100, facecolor='w', edgecolor='k')
    #pos = nx.nx_agraph.graphviz_layout(g)
    
    nodi_size = [((math.sqrt(v) / 6) * 2000) for v in d.values()]
    pos = nx.nx_agraph.graphviz_layout(g)
    #print(nodi_size)
    nx.draw(g, pos=pos, arrows=True, width=0.1, node_size=nodi_size, \
    node_color='lightblue', linewidths=0.25, font_size=10, with_labels=True, scale = math.ceil(math.sqrt(g.number_of_nodes()) / 8))
    
    plt.savefig(domain + '.png')
    plt.show()
    #print(find_all_urls_single_page(website,soup))
    #print_all_headers(headings)
    #print_specific_header(headings, "h2")
    #print_all_headers_count(headings)

if __name__ == "__main__":
    #main("https://www.padok.fr", "www.padok.fr")
    main("https://primates.dev", "primates.dev")
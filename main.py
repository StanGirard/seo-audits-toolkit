import requests
import re
import math
from bs4 import BeautifulSoup
import urllib.parse
import networkx as nx
from operator import itemgetter
import matplotlib.pyplot as plt
from bokeh.io import output_file, show
from bokeh.plotting import figure, from_networkx
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, LinearColorMapper)
from bokeh.palettes import Spectral4, Spectral8
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.layouts import gridplot
import numpy as np
import seaborn as sns
palette = sns.color_palette("hls", 99)
pal_hex_lst = palette.as_hex()



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
                        list_urls[extract_path(url)].append(extract_path(url_joined))
                        
                        add_edge(list_urls, url_joined, domain)
            return list_urls
        
    return list_urls
    
    
def generate_graph_internal_link(website):
    domain = urllib.parse.urlparse(website).netloc
    urls = add_edge({}, website,domain )
    
    g = nx.Graph(urls)
    d = dict(g.degree)
    size = g.number_of_nodes()
    print(g.degree)
    max_connection = max(d.values())
    
    colors = [i[1]/ max_connection for i in g.degree]


    plt.figure(num=None, figsize=(30 * math.ceil(math.sqrt(size) / 8), 20 * math.ceil(math.sqrt(size)/ 8 )), dpi=100, facecolor='w', edgecolor='k')    
    nodi_size = [((math.sqrt(v) / 6) * 3000) for v in d.values()]
    pos = nx.nx_agraph.graphviz_layout(g)
    
    nx.draw(g, pos=pos, arrows=True, width=0.1, node_size=nodi_size, \
    node_color=colors, linewidths=0.25, font_size=10, with_labels=True, scale = math.ceil(math.sqrt(g.number_of_nodes()) / 8))
    
    plt.savefig(domain + '.png')
    plt.show()        

def generate_graph_internal_link_interactive(website):
    domain = urllib.parse.urlparse(website).netloc
    urls = add_edge({}, website,domain )
    
    g = nx.Graph(urls)

    d = dict(g.degree)
    maxi = max(d.values())
    node_size = {k:math.ceil(math.sqrt(int(v)) / 8) * 15 for k,v in d.items()}
    node_color = {k:math.ceil((v / maxi) * 99 ) for k, v  in d.items()}
    mapper = LinearColorMapper(palette=pal_hex_lst, low=0, high=99)
    #print(node_color)
    #print(node_size)
    nx.set_node_attributes(g, d, 'connection')
    nx.set_node_attributes(g, node_size, "node_size")
    nx.set_node_attributes(g, node_color, "node_color")
    

    
    plot = figure(title="Maillage Interne " + domain, plot_width=1200, plot_height=800,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    p = gridplot([[plot]], sizing_mode='stretch_both')


    
    
    graph = from_networkx(g,nx.spring_layout, scale=2)
    node_hover_tool = HoverTool(tooltips=[("urls", "@index"), ("Connection", "@connection")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
    plot.toolbar.active_scroll = "auto"

    


    
    graph.node_renderer.hover_glyph = Circle(size=20,fill_color=Spectral4[1])

    
    graph.edge_renderer.hover_glyph = MultiLine(line_color=Spectral8[6],line_width=1)

    # graph.selection_policy = NodesAndLinkedEdges()
    # graph.inspection_policy = EdgesAndLinkedNodes()

    graph.edge_renderer.glyph = MultiLine( line_alpha=0.8, line_width=0.1)
    graph.node_renderer.glyph = Circle(size='node_size', fill_color={'field': 'node_color', 'transform': mapper})

    graph.inspection_policy = NodesAndLinkedEdges()
    
    plot.renderers.append(graph)

    output_file(domain + ".html")
    show(p)
   

def main(website):
    generate_graph_internal_link_interactive(website)
    #print(find_all_urls_single_page(website,soup))
    #print_all_headers(headings)
    #print_specific_header(headings, "h2")
    #print_all_headers_count(headings)

if __name__ == "__main__":
    main("https://www.padok.fr")
    #main("https://souslapluie.fr")
    #main("https://primates.dev")
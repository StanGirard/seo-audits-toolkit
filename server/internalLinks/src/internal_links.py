import logging
import math
import urllib
import json
import urllib.parse
from datetime import datetime, timedelta

import networkx as nx
import requests
import seaborn as sns
from bokeh.embed import components
from bokeh.layouts import row
from bokeh.models import (BoxZoomTool, Circle, ColorBar, ColumnDataSource,
                          DataTable, HoverTool, MultiLine, Range1d, ResetTool,
                          TableColumn)
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.palettes import Spectral4, Spectral6, Spectral8
from bokeh.plotting import figure, from_networkx
from bokeh.transform import linear_cmap
from bs4 import BeautifulSoup
from bokeh.embed import json_item


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
palette = sns.color_palette("hls", 99)
pal_hex_lst = palette.as_hex()


def find_all_urls_single_page(source, soup):
    list_urls = {source: {"urls": {}, "count": 0, "broken": 0}}
    for link in soup.findAll('a'):
        url = urllib.parse.urljoin(source, link.get('href'))
        if url not in list_urls[source]['urls']:
            status_code = request_status_code(url)
            if status_code == 200:
                list_urls[source]["urls"][url] = {"status": 200, "count": 1}
            else:
                list_urls[source]["urls"][url] = {
                    "status": status_code, "count": 1}
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


def add_edge(list_urls, url, domain, maximum=500):

    if len(list_urls) > maximum:
        return list_urls
    if domain not in url:
        logging.info(url + " not in domain")
        return

    if extract_path(url) not in list_urls and domain in url and (url.startswith("https://" + domain) or url.startswith("http://" + domain)):
        list_urls[extract_path(url)] = []
        logging.info("Requesting " + url)
        soup = request_parse(url)
        if soup:
            for link in soup.find_all('a'):
                url_joined = urllib.parse.urljoin(url, link.get('href'))

                if url_joined.startswith("https://" + domain) or url_joined.startswith("http://" + domain):
                    if url_joined not in list_urls[extract_path(url)]:
                        list_urls[extract_path(url)].append(
                            extract_path(url_joined))

                        add_edge(list_urls, url_joined, domain, maximum)
            return list_urls

    return list_urls


def generate_graph_internal_link_interactive(website, maximum):
    domain = urllib.parse.urlparse(website).netloc
    urls = add_edge({}, website, domain, maximum)

    # Generating graph and dict of degrees
    g = nx.Graph(urls)
    d = dict(g.degree)

    # Adding table
    table = dict(url=[k for k, v in d.items()],
                 count=[v for k, v in d.items()])
    source = ColumnDataSource(table)
    columns = [
        TableColumn(field="url", title="URL"),
        TableColumn(field="count", title="Count"),
    ]
    data_table = DataTable(source=source, columns=columns,
                           width=400, height_policy="max")

    # Generating node size and color
    maxi = 1
    if len(d.values()) > 0:
        maxi = max(d.values())
    node_size = {k: max(5, math.ceil((v / maxi) * 30)) for k, v in d.items()}
    node_color = {k: v for k, v in d.items()}
    mapper = linear_cmap(field_name='node_color', palette=Spectral6, low=min(
        node_color.values()), high=max(node_color.values()))
    nx.set_node_attributes(g, d, 'connection')
    nx.set_node_attributes(g, node_size, "node_size")
    nx.set_node_attributes(g, node_color, "node_color")

    plot = figure(title="Maillage Interne " + domain, plot_width=1200, plot_height=800,
                  x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1), sizing_mode='stretch_both')
    p = row([data_table, plot])
    graph = from_networkx(g, nx.spring_layout, scale=2)
    node_hover_tool = HoverTool(
        tooltips=[("urls", "@index"), ("Connection", "@connection")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
    plot.toolbar.active_scroll = "auto"

    graph.node_renderer.hover_glyph = Circle(size=20, fill_color=Spectral4[1])
    graph.edge_renderer.hover_glyph = MultiLine(
        line_color=Spectral8[6], line_width=1)
    graph.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=0.03)
    graph.node_renderer.glyph = Circle(size='node_size', fill_color=mapper)

    graph.inspection_policy = NodesAndLinkedEdges()
    color_bar = ColorBar(
        color_mapper=mapper['transform'], width=8,  location=(0, 0))
    plot.add_layout(color_bar, 'right')
    plot.renderers.append(graph)
    return json.dumps(json_item(p, "myplot"))

if __name__ == "__main__":
    script, div = generate_graph_internal_link_interactive("https://primates.dev", 10)
    print(div)
    print(script)

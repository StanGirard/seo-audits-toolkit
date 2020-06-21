import math
from datetime import datetime, timedelta

from bokeh.embed import components
import urllib.parse
import networkx as nx
from bokeh.plotting import figure, from_networkx
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine,  Range1d, ResetTool,  ColorBar,
                          ColumnDataSource, DataTable, TableColumn)
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral4, Spectral8, Spectral6
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.layouts import row
from flask import render_template

from toolkit.db import graphs
from toolkit.lib.http_tools import request_parse, request_status_code
import seaborn as sns
import logging

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
    return p, domain


def update_or_insert_graph_in_db(conn, urls, maximum, update=False):
    """Update or inserts html in the DB

    Arguments:
        conn {Connection} -- DB connector
        urls {string} -- Root Domain
        maximum {int} -- Maximum number of urls to crawl

    Keyword Arguments:
        update {bool} -- update or insert (default: {False})

    Returns:
        HTML Render -- Renders the Graph
    """
    plot, domain = generate_graph_internal_link_interactive(urls, maximum)
    script, div = components(plot)
    graphs.update_url_db(conn, (datetime.now().strftime(
        "%m/%d/%Y, %H:%M:%S"), script, div, "FINISHED", urls))
    return render_template("bokeh.html", script=script, div=div, domain=domain, template="Flask", time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))


def generate_interactive_graph(conn, urls, relaunch, maxi_urls):
    if urls is None:
        return "Empty Url paramaters"
    maximum_urls = 500
    if maxi_urls is not None:
        maximum_urls = int(maxi_urls)
    stopped, already_exists = graphs.check_status_url(conn, urls, "FINISHED")

    if stopped == True:

        # If not first time
        if already_exists:
            query_result = graphs.select_visited(conn, urls)
            # ALREADY VISITED IN THE LAST 24 HOURS

            if datetime.strptime(query_result[0][2], '%m/%d/%Y, %H:%M:%S') + timedelta(hours=24) > datetime.now() and relaunch != "True":
                return render_template("bokeh.html", script=query_result[0][3], div=query_result[0][4], domain=urllib.parse.urlparse(query_result[0][1]).netloc, template="Flask", time=datetime.strptime(query_result[0][2], '%m/%d/%Y, %H:%M:%S'))

            # More than 24 hours or parameter redo is True
            if (datetime.strptime(query_result[0][2], '%m/%d/%Y, %H:%M:%S') + timedelta(hours=24) < datetime.now() or relaunch == "True"):
                graphs.update_running_db(conn, ("RUNNING", urls))
                return update_or_insert_graph_in_db(conn, urls,  maximum_urls, True)

        # If first time
        else:
            graphs.insert_url_db(conn, (urls, datetime.now().strftime(
                "%m/%d/%Y, %H:%M:%S"), "", "", "RUNNING"))
            return update_or_insert_graph_in_db(conn, urls, maximum_urls)
    else:
        return "JOB IS ALREADY RUNNING. PLEASE WAIT AND REFRESH."

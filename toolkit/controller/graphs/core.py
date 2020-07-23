import logging
import math
import urllib
import urllib.parse
from datetime import datetime, timedelta

import networkx as nx
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
from flask import render_template, request
from sqlalchemy import update
from toolkit import dbAlchemy as db
from toolkit.lib.api_tools import generate_answer
from toolkit.lib.http_tools import request_parse, request_status_code
from toolkit.models import Graphs

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
    return render_template("graphs/bokeh.jinja2", script=script, div=div, domain=domain, template="Flask", time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))






def update_or_insert_graph_in_db( urls, maximum, updating=False):
    plot, domain = generate_graph_internal_link_interactive(urls, maximum)
    script, div = components(plot)
    conn = db.engine.connect()
    smt = update(Graphs).where(Graphs.urls == urls).values(script= script, 
            div = div, begin_date=datetime.now(), status_job="FINISHED")
    conn.execute(smt)
    return render_template("graphs/bokeh.jinja2", script=script, div=div, domain=domain, template="Flask", time=datetime.now())

def generate_interactive_graph(urls, relaunch,task, maxi_urls):
    if urls is None:
        return "Empty Url paramaters"
    maximum_urls = 500
    if maxi_urls is not None:
        maximum_urls = int(maxi_urls)
    urls_exists = Graphs.query.filter(Graphs.urls == urls).count()
    if urls_exists > 0:
        stopped = Graphs.query.filter(Graphs.urls == urls and Graphs.status_job == "RUNNING").first()
        if stopped.status_job == "FINISHED":
            query_result = Graphs.query.filter(Graphs.urls == urls and Graphs.status_job == "RUNNING").first()
            # ALREADY VISITED IN THE LAST 24 HOURS

            if query_result.begin_date + timedelta(hours=24) > datetime.now() and relaunch != "True":
                return render_template("graphs/bokeh.jinja2", script=query_result.script, div=query_result.div, domain=urllib.parse.urlparse(query_result.urls).netloc, template="Flask", time=query_result.begin_date)

            # More than 24 hours or parameter redo is True
            if query_result.begin_date + timedelta(hours=24) < datetime.now() or relaunch == "True":
                conn = db.engine.connect()
                smt = update(Graphs).where(Graphs.urls == urls).values(status_job="RUNNING")
                conn.execute(smt)
                return update_or_insert_graph_in_db(urls,  maximum_urls, True)

        else:
            return {"error": "You graph is being generated. Please wait"}

    else:
        new_graph = Graphs(
            urls = urls, script="", div="", status_job = "RUNNING",task_id=task, begin_date=datetime.now()
        )
        db.session.add(new_graph)
        db.session.commit()
        return update_or_insert_graph_in_db(urls, maximum_urls)

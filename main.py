from seo.core import generate_graph_internal_link_interactive 
from bokeh.io import  show

if __name__ == "__main__":
    
    p, domain = generate_graph_internal_link_interactive("https://primates.dev", 500)
    show(p)
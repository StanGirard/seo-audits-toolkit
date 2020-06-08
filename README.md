# SEOToolkit

![](examples/example.png)

This seo toolkit is a collection of multiple toos to help you in SEO improvement. It is an easy to use API.
## Installation

You need **Python3**

```Bash
git clone https://github.com/StanGirard/SEOToolkit
cd SEOToolkit
```

Then install dependencies

```Bash
pip install -r requirements.txt
```

## Running Flask

```Bash
python3 flask_api
```

This will expose one endpoint:
- `localhost:5000/api/graph`

### Parameters

-  `/api/graph?url=https://primates.dev` will crawl the website and respond with the graph as html
-  `/api/graph?url=https://primates.dev&redo=True` will force the crawling. Doesn't crawl if less than 24 hours
-  `/api/graph?url=https://primates.dev&max=10` stops after visiting 10 pages. (Default=500)

## TODO

- [ ] Not downloading images when they are linked
- [ ] Async requests
- [ ] Implement Scrapy for better perf

Have fun ! 

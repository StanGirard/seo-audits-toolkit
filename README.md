# SEOToolkit

![](examples/example.png)

This seo toolkit is a collection of multiple tools to help you in your quest for a better SEO. It is an easy to use API.

I've grown tired of SEO agencies making us pay hundreds of euros for simple tools. I decided to develop an API to help users find issues in their website and increase their SEO for free. It can, of course, be used for anything else.

- [SEOToolkit](#seotoolkit)
  - [Installation](#installation)
  - [Updating](#updating)
  - [Running Flask](#running-flask)
  - [Endpoints](#endpoints)
    - [Graphs](#graphs)
    - [SERP - Search Engine Result Page Rank](#serp---search-engine-result-page-rank)
    - [Keywords Query Finder](#keywords-query-finder)
    - [Extracts](#extracts)
      - [Headers](#headers)
      - [Links](#links)
      - [Images](#images)
  - [TODO](#todo)

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

## Updating

Please delete the file visited.db if you have any issues when updating. 

## Running Flask

```Bash
python3 flask_api
```

This will expose six endpoints:
- `localhost:5000/api/graph`
- `localhost:5000/api/extract/headers`
- `localhost:5000/api/extract/links`
- `localhost:5000/api/extract/links/website`
- `localhost:5000/api/serp`
- `localhost:5000/api/analysis/keywords`

## Endpoints

---

### Graphs

-  `/api/graph?url=https://primates.dev` will crawl the website and respond with the graph as html
-  `/api/graph?url=https://primates.dev&redo=True` will force the crawling. Doesn't crawl if less than 24 hours
-  `/api/graph?url=https://primates.dev&max=10` stops after visiting 10 pages. (Default=500)

--- 

### SERP - Search Engine Result Page Rank

- `/api/serp?domain=primates.dev&query=parse api xml response&tld=com&lang=en` will give the rank of your website based on a query. tld and lang are not required. 
Default values are **.com** and **en**

```JSON
{
  "pos": 2, 
  "url": "https://primates.dev/parsing-an-api-xml-response-data-python/"
}
```

---

### Keywords Query Finder

This endpoint allows you to find all the keywords used on the pages found in a Google result for a specific query

- `/api/analysis/keywords?query=parse api xml response`

It returns the most used Monograms, Bigrams and Tigrams and the pages. It will visit the first 20 pages of the results.

```JSON
{
  "Bigram": [
    {
      "frequency": 102, 
      "keyword": "xml document"
    }, 
    {
      "frequency": 99, 
      "keyword": "xml response"
    }, 
    {
      "frequency": 75, 
      "keyword": "xml parser"
    }, 
    {
      "frequency": 70, 
      "keyword": "stack overflow"
    }, 
    {
      "frequency": 68, 
      "keyword": "parsing xml"
    }, 
    ...
  ], 
  "Monogram": [
    {
      "frequency": 1506, 
      "keyword": "xml"
    }, 
    {
      "frequency": 445, 
      "keyword": "data"
    }, 
    {
      "frequency": 406, 
      "keyword": "parser"
    }, 
    {
      "frequency": 392, 
      "keyword": "api"
    }, 
    {
      "frequency": 374, 
      "keyword": "response"
    }, 
    {
      "frequency": 357, 
      "keyword": "name"
    }, 
    ...
  ], 
  "Trigram": [
    {
      "frequency": 45, 
      "keyword": "xml etree elementtree"
    }, 
    {
      "frequency": 30, 
      "keyword": "xml version encoding"
    }, 
    {
      "frequency": 30, 
      "keyword": "version encoding utf"
    }, 
    ...
  ]
}
```

---

### Extracts

#### Headers

- `/api/extract/headers?url=https://primates.dev` returns all the headers of the page

```JSON
{
  "h1": {
    "count": 0, 
    "values": []
  }, 
  "h2": {
    "count": 15, 
    "values": [
      "Help fight diseases with your computer", 
      "A Twitter Crawler and News Indexer", 
      "Find every social account of a user", 
      "How to point a domain name to a server?"
    ]
  }, 
 ...
  "h6": {
    "count": 0, 
    "values": []
  }
}
```

#### Links

- `/api/extract/links?url=https://primates.dev`

This will give you all the links on the page and their status codes.

```JSON
{
  "200":
  [
    "https://primates.dev","https://primates.dev/become-an-author/",
    "https://www.facebook.com/primatesDev","https://primates.dev/tag/python/", ...
  ],
"500":["javascript:;"]
}
```

- `api/extract/links/website?url=https://primates.dev&max=50` 

This will give you all the links found on your website. 

```JSON
{
  "domain_name":"primates.dev",
  "external_urls":
    {
      "results":["https://www.linkedin.com/shareArticle","https://archive.org/web/","https://git-scm.com/book",...],
      "total":90
    },
  "internal_urls":
    {
      "results":
        ["https://primates.dev/","https://primates.dev/brave-a-web-browser-that-pays-its-users-and-respects-privacy/",...],
      "total":67
    },
    "pages_visited":51,
    "time_crawl":13.310942938551307,
    "total":157
}
```
#### Images

- `/api/extract/images?url=https://primates.dev`

This will give you all the image links of a page and a summary of the page.

```JSON
{
  "images":
    [
      {"alt":"Primates","url":"https://primates.dev/content/images/size/w600/2020/02/monkey.png"},
      {"alt":"10 Tips on How to choose a domain name for your business","url":"https://primates.dev/content/images/size/w1000/2020/06/SEO.jpg"},
      ...
    ],
  "summary":{"duplicates":17,"missing_alt":0,"missing_title":37,"total":37}}
}
```

## TODO

- [ ] Not downloading images when they are linked
- [ ] Async requests
- [ ] Implement Scrapy for better perf
- [ ] Clean Code regarding DB Interactions

Have fun ! 

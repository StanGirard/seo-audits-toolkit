<p align="center"><img src="./examples/OSAT.png" width="180px" /></p>


# Open source SEO Audits Toolkit

**OSAT** is a collection of multiple tools to help you in your quest for a better SEO. All of these tools have been grouped into a single web app.

I've grown tired of SEO agencies making us pay hundreds of euros for simple tools. I decided to develop **OSAT** to help users find issues in their website and increase their SEO for free. 

<p align="center"><img src="./examples/seotoolkit.gif" width="600px" /></p>

## Why you need it


- It's **free** to use, easy and open source. No credit cards required.
- It has a growing list of features
- It's easy to install

## Features


- **Lighthouse Score**: Run [Lighthouse](https://developers.google.com/web/tools/lighthouse) Audits and keep track of your scores
- **SERP Rank** - Get the rank of your website on google for specific queries
- **Keywords Finder** - Finds all the Mono,Bi and Trigrams associated to a specific request. Helps you write content faster.
- **Internal Links Graphs** - Creates a graph of your website showing all the connections between your pages.
- **Extract Headers/Links/Images** - Easily extract all the links on your website and their status codes, the headers of a page and all the images.



## Installation

You need: 
- **Python3**
- **[Redis Server](https://redis.io/topics/quickstart)**


```Bash
git clone https://github.com/StanGirard/SEOToolkit
cd SEOToolkit
```

Then install dependencies

```Bash
pip install -r requirements.txt
```

## Running

### Flask
```Bash
python3 run.py
```

### Redis Server
```Bash
redis-server
```

### Celery Worker
```Bash
celery worker -A celery_worker.celery --loglevel=info
```



## Dashboard

You can access the dashboard by going to [localhost:5000](http://localhost:5000)

## Config

If needed create a `.env` file with information that you would like to overload from config.py

## Screenshots

### SERP Rank

![](examples/SERP-rank.png)

### Internal Links Graphs

![](examples/graphs.png)

### Keywords Finder

![](examples/keywords-finder.png)

### Lighthouse Audit

![](examples/lighthouse-primates.png)

### Images Extractor

![](examples/images.png)

## API

### Lighthouse

| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Audits | `/api/audit/lighthouse/score` | `None` |
| **GET**     | Audit by Id | `/api/audit/lighthouse/score/<id>` | `id` |
| **POST**     | Generates an Audit | `/api/audit/lighthouse/score` | `url` |

### Extract
#### Headers
| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Extracted Headers | `/api/extract/headers` | `None` |
| **GET**     | Headers by Id | `/api/extract/headers/<id>` | `id` |
| **POST**     | Extract Header from URL | `/api/extract/headers` | `url` |
| **POST**     | Deletes Headers by Id | `/api/extract/headers/delete` | `id` |

#### Status Code Links
| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Links status extracted from pages| `/api/extract/links` | `None` |
| **GET**     | Links Status by ID | `/api/extract/links/<id>` | `id` |
| **POST**     | Extracts link status from URL | `/api/extract/links` | `url` |
| **POST**     | Delete Link status by ID | `/api/extract/links/delete` | `id` |

#### Internal & External Links
| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Internal & External links extracted from pages | `/api/extract/links/website` | `None` |
| **GET**     | Internal & External by ID | `/api/extract/links/website/<id>` | `id` |
| **POST**     | Extracts Internal & External links from URL | `/api/extract/links/website` | `url` |
| **POST**     | Deletes Internal & External links by ID | `/api/extract/links/website/delete` | `id` |

#### Images
| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Images extracted from pages | `/api/extract/images` | `None` |
| **GET**     | Images by ID | `/api/extract/images/<id>` | `id` |
| **POST**     | Extracts Images from URL | `/api/extract/images` | `url` |
| **POST**     | Deletes Images by ID | `/api/extract/images/delete` | `id` |

### Internal Linking Graphs
| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Internal Linking Graphs generated | `/api/graphs` | `None` |
| **GET**     | Graphs by ID | `/api/graphs/<id>` | `id` |
| **POST**     | Extracts graph from domain | `/api/graphs` | `domain` |
| **POST**     | Deletes Graphs by ID | `/api/graphs/delete` | `id` |

### Query Keywords Generator
| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Keywords generated | `/api/keywords` | `None` |
| **GET**     | Keywords by ID | `/api/keywords/<id>` | `id` |
| **POST**     | Extracts keywords from query | `/api/keywords` | `query` |
| **POST**     | Deletes Keywords by ID | `/api/keywords/delete` | `id` |

### Search Engine Result Page Rank
| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Ranks | `/api/rank` | `None` |
| **POST**     | Extracts ranks from query and domain | `/api/rank` | `query` & `domain` |
| **POST**     | Deletes ranks by ID | `/api/rank/delete` | `id` |




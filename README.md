# SEOToolkit

![](examples/seotoolkit.gif)

This seo toolkit is a collection of multiple tools to help you in your quest for a better SEO. It is an easy to use API.

I've grown tired of SEO agencies making us pay hundreds of euros for simple tools. I decided to develop an API to help users find issues in their website and increase their SEO for free. It can, of course, be used for anything else.

- [SEOToolkit](#seotoolkit)
  - [Installation](#installation)
  - [Running](#running)
  - [Dashboard](#dashboard)
  - [Config](#config)
  - [Features](#features)
  - [Screenshots](#screenshots)
    - [SERP Rank](#serp-rank)
    - [Internal Links Graphs](#internal-links-graphs)
    - [Keywords Finder](#keywords-finder)
    - [Lighthouse Audit](#lighthouse-audit)
    - [Images Extractor](#images-extractor)
  - [API](#api)

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

or you can use Docker

```Bash
docker build -t seo-toolkit:latest .
```

## Running

```Bash
flask run
```

or with docker

```Bash
docker run -d -p 5000:5000 seo-toolkit:latest
```

## Dashboard

You can access the dashboard by going to [localhost:5000](http://localhost:5000)

## Config

If needed create a `.env` file with information that you would like to overload from config.py


## Features

- **Lighthouse Score**: Run [Lighthouse](https://developers.google.com/web/tools/lighthouse) Audits and keep track of your scores
- **SERP Rank** - Get the rank of your website on google for specific queries
- **Keywords Finder** - Finds all the Mono,Bi and Trigrams associated to a specific request. Helps you write content faster.
- **Internal Links Graphs** - Creates a graph of your website showing all the connections between your pages.
- **Extract Headers/Links/Images** - Easily extract all the links on your website and their status codes, the headers of a page and all the images.


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

The API won't be maintained for now as I am moving towards the dashboard. Existing endpoints will still be working. If you need informations on the API please visit an [older](https://github.com/StanGirard/SEOToolkit/tree/ed6a59513921d5e58f3c69839274cd59b1e33fb2) version of the project.

---
layout: default
title: API
nav_order: 3
description: "OSAT is an open source audit toolkit to help you improve your seo"
permalink: /api
last_modified_date: 2020-07-24T17:54:08+0000
---

1. TOC
{:toc}

## API
{: .no_toc }

### Lighthouse

| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Audits | `/api/audit/lighthouse/score` | `None` |
| **GET**     | Audit by Id | `/api/audit/lighthouse/score/<id>` | `id` |
| **POST**     | Generates an Audit | `/api/audit/lighthouse/score` | `url` |

---

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

---

### Internal Linking Graphs

| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Internal Linking Graphs generated | `/api/graphs` | `None` |
| **GET**     | Graphs by ID | `/api/graphs/<id>` | `id` |
| **POST**     | Extracts graph from domain | `/api/graphs` | `domain` |
| **POST**     | Deletes Graphs by ID | `/api/graphs/delete` | `id` |

---

### Query Keywords Generator

| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Keywords generated | `/api/keywords` | `None` |
| **GET**     | Keywords by ID | `/api/keywords/<id>` | `id` |
| **POST**     | Extracts keywords from query | `/api/keywords` | `query` |
| **POST**     | Deletes Keywords by ID | `/api/keywords/delete` | `id` |

---

### Search Engine Result Page Rank

| METHOD       | DESCRIPTION           | ENDPOINT           | PARAMS  | 
| :-------------: |-------------| -----|-----|
| **GET**     | All Ranks | `/api/rank` | `None` |
| **POST**     | Extracts ranks from query and domain | `/api/rank` | `query` & `domain` |
| **POST**     | Deletes ranks by ID | `/api/rank/delete` | `id` |

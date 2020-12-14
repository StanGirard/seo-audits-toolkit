---
layout: default
title: Beta
nav_order: 4
description: "OSAT is an open source audit toolkit to help you improve your seo"
permalink: /beta
has_children: true
last_modified_date: 2020-07-24T17:54:08+0000
---

{: .fs-9 }
<p align="center"><img src="/examples/OSAT.png" width="180px" /></p>
{: .fs-6 .fw-300 }

[Get started now](#installation){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/StanGirard/seo-audits-toolkit){: .btn .fs-5 .mb-4 .mb-md-0 }

---

1. TOC
{:toc}


## Introduction

In order to be able to go further with this project. I need to change the backend framework. 
I've been using Flask for the backend and frontend. However I'd like to change and go towards React for the front and a dedicated backend framework.

### Django

Django has many features that are pretty good for the long terme. 
It will allow me to onboard new developers faster on the project and it will allow me to more easily integrate authentification and other features.

### Useful Endpoints

After running the application, you'll find several useful endpoints. 

- [https://localhost:8000/admin](https://localhost:8000/admin) which is the Django Admin Framework
- [https://localhost:8000/](https://localhost:8000/) which is the API Rest Framework

### Module used in Django

I've installed many modules to allow the project to have many more features.

- [Rest Framework](https://www.django-rest-framework.org/#) which allows us to use Django for easily building Web APIs
- [Cors Headers](https://pypi.org/project/django-cors-headers/) to easily allow cross site while developing
- [Django Filters](https://django-filter.readthedocs.io/en/stable/guide/install.html) allows to easily add filters to REST endpoint


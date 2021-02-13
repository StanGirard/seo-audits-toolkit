<p align="center"><img src="./docs/images/OSAT.png" width="180px" /></p>


# Open source Audits Toolkit

**OSAT** is a collection of tools created help you in your quest for a better website. All of these tools have been grouped into a single web app.

I've grown tired of SEO agencies making us pay hundreds of euros for simple tools. I decided to develop **OSAT** to help users find issues on their website and increase their SEO for free. 

<p align="center"><img src="./docs/images/osat-demo.gif" width="700px" /></p>

## Why you need it


- It's **free**, easy and open source. 
- It has a growing list of features
- It's easy to install

## Features

- **Authentification** - A fully featured authentification system for the front & back
- **RBAC/Organizations** - Create different organizations and give different access to each org to your users.
- **Lighthouse Score** -  Run [Lighthouse](https://developers.google.com/web/tools/lighthouse) Audits and keep track of your scores
- **SERP Rank** - Get the rank of your website on google for specific queries
- **Keywords Finder** - Find all the keywords of an article.
- **Extract Headers/Links/Images** - Easily extract all the links on your website and their status codes, the headers of a page and all the images.
- **Sitemap Extractor** - Extract all the urls of a website from its sitemap
- **Summarizer** - Summarize any text from any length. Awesome for excerpt ! 
- **Security Audit** - Audit Headers, Redirect, etc to make sure you website is secure.



## Installation

```Bash
git clone https://github.com/StanGirard/seo-audits-toolkit
cd seo-audits-toolkit
docker-compose --env-file .env-example build
docker-compose --env-file .env-example up -d
```

Init the project

```Bash
docker exec -it osat-server python manage.py loaddata init_data.json
```


## Dashboard

You can access the dashboard by going to [localhost:3000](http://localhost:3000)

**Login**: admin
**Password**: admin
## Config

If needed create a `.env` file with information that you would like to change

## Configuration


### Create organization

You need to go to `Org -> Organization` and create a new organization. You can create as many as you want. Organization are used in order to implement RBAC in the project and only display information about an organization to users of this organization. Here is a quicklinkg to access it [http://localhost:8000/admin/org/website/](http://localhost:8000/admin/org/website/)


### Add user to organization

Once your organization is created. You need to add your users to this organization. 
Go to `Organizations -> Organizations Users` and add your users to the organization you want. [http://localhost:8000/admin/organizations/organizationuser/](http://localhost:8000/admin/organizations/organizationuser/)

## Useful Links

- **Webapp** [http://localhost:3000](http://localhost:3000)
- **Admin Dashboard** [http://localhost:8000/admin](http://localhost:8000/admin)
- **Swagger like interface** [http://localhost:8000](http://localhost:8000)


## Contributions

Please feel free to add any contribution.
If you've been working on a script that could be integrated in this app. Please feel free to do it. Don't hesitate to open issues to ask questions. I've tried to document the code as much as I could to ease the integration

### Backend 
You can just add a django module and I'll take care of intregrating it in the front.
### Frontend
I've used React Admin to build the front-end. If you want to help me improve the UI or add new functionnalites. Please feel free to contribute.

## Disclaimers

I'm not a python nor a frontend developer.












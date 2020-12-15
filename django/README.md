## Introduction

Useful endpoints:
- https://localhost:8000/admin -> Django Admin framework
- https://localhost:8000/ -> API REST framework

## Installation

- Redis-server running


### Django 

```Bash
cd osat
pip3 install -r requirements.txt
pip3 install celery
```

### Database 

Go to `osat/settings.py`
Change the values you need in 
```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'osat',
        'USER': 'postgres',
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "TEST"),
        'HOST': 'osat.ctcghdbvsxw2.eu-west-3.rds.amazonaws.com',
        'PORT': '5432',
    }
}
```

### Running

**You need to have a Redis server running on your machine.**


If you want to run the project.

- `python manage.py migrate` 
- `python manage.py createsuperuser`
- `python manage.py runserver`

And in another terminal run:

`celery -A osat  worker -l info`

`celery -A osat beat -l info`

### Changes to models

If you make a change to a model simply run

- `python3 manage.py makemigrations`
- `python3 manage.py migrate` 


### Creating a new plugin

- `python3 manage.py startapp <nameofyourplugin>`

This will create a new folder.

In `Django_SEO/settings.py` add your app in INSTALLED_APPS:

```Python
INSTALLED_APPS = [
    'extractor.apps.ExtractorConfig', ### This is the app from the Extractor Folder
    ....
```

Copy and modify the code from extractor to help you start:
- admin.py -> Change the model
- serializers -> Adapt the create method with your celery task
- tasks -> Modify to suit your needs
- Views -> Change the filter and ordering fields

Then you need to add your app to `osat/urls.py` ->
```Python
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'api/extractor', ExtractorViewSet)
### Add your root here
```


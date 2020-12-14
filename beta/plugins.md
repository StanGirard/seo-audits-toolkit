---
layout: default
title: Create a plugin
parent: Beta
nav_order: 2
---
1. TOC
{:toc}

Before creating a plugin, make sure that you Django instance is correctly running and that you've followed everything in the [django installation section](/beta/django). 

---

In order to create a new plugin you first need to run the following command at the root of the project (where `manage.py` is)

- `python3 manage.py startapp <nameofyourplugin>`

This will create a new folder with a bunch of files already created. Django is a robust frameworks that helps a lot when you need to create new app in your project.

You then need to declare your application in the django root project. In order to do that you'll need to add the following in the `Django_SEO/settings.py` 

```Python
INSTALLED_APPS = [
    'extractor.apps.ExtractorConfig', ### This is the app from the Extractor Folder
    '<nameofyourplugin>.apps.<nameofyourplugin>Config',
    ....
```

This tells Django to look at your new app and integrate it. It is required. Without it, your application will not work.

---
#### Admin

In your `admin.py` file, add all the models that you want to be accessible from Django Admin

```Python
from django.contrib import admin

from .models import <yourModel>

admin.site.register(<yourModel>)
etc...
```

You'll be able to manage your models directly from the Django Admin located at [https://localhost:8000/admin](https://localhost:8000/admin). Don't forget your super user login and password.

---
#### Models

The `models.py` file is where you declare your models.

I'll not talk a lot about it. Just look at the [documentation](https://docs.djangoproject.com/en/3.1/topics/db/models/) for the fields.

Just remember to run the following commands after each changes:

- `python3 manage.py makemigrations`
- `python3 manage.py migrate` 

---
#### Serializers

Serializers are a powerful feature of [Django Rest Framework](https://www.django-rest-framework.org/)

I highly recommend looking at these good tutorial on [Serializers](https://www.django-rest-framework.org/tutorial/1-serialization/)


I encourage you to copy and paste what I've done in the Extractor app for the `serializers.py` file.

Let's have a look at the file

```Python
class ExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extractor
        fields = ['id','url', 'result', 'type_audit', 'task_id', 'status_job', 'begin_date']

    def create(self, validated_data):
        ## Creates the celery task
        extractor_task = extractor_job.delay(validated_data["url"],validated_data["type_audit"])
        
        ## Creates the Save to DB
        newExtractor = Extractor.objects.create(
        url = validated_data["url"],status_job="SCHEDULED",task_id=str(extractor_task.id), result="", begin_date=timezone.now(), type_audit=validated_data["type_audit"]
        )
        
        
        return newExtractor
```

What I've done is that I've overriden the create method which is used when making a POST request.
What happens is as follows:
- I created a celery task and I pass the values that I need.
- I create an Extractor Object based on the model and return it.

By overriding the create method, I've added an asynchronous task with celery.

---
#### Tasks

We've seen in the `serializers.py` file that I've overrident the create method and added a task. We'll look at how to add a new task.

First of all copy the content of `task.py` from the Extractor app.

Let's look at it
```Python
@task(bind=True, name="extractor_job")
def extractor_job(self,url, task_type):
    print(task_type)
    Extractor.objects.filter(task_id=self.request.id).update(status_job="RUNNING")
    result = None
    if (task_type == "HEADERS"):
        result = find_all_headers_url(url)
    elif (task_type == "IMAGES"):
        result = find_all_images(url)
    elif (task_type == "LINKS"):
        result = find_all_links(url)
    Extractor.objects.filter(task_id=self.request.id).update(result=str(result), status_job="FINISHED")
    return "Hello World!"
```

What it does is fairly simple:
- `@task(bind=True, name="<name>")` declares the following function as a task.
- `Extractor.objects.filter(task_id=self.request.id).update(status_job="RUNNING")` changes the status job to RUNNING
- Then depending on the `task_type` I call different methods.
- `Extractor.objects.filter(task_id=self.request.id).update(result=str(result), status_job="FINISHED")` adds the results and changes the status of the job.
- `return "Hello World!"`  because we don't care about the result :D 

---
#### Views 

The `views.py` is where we declare our REST endpoint.

Let's look at what I've done in Extractor
```Python
class ExtractorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Extractor.objects.all().order_by('-begin_date')
    serializer_class = ExtractorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'type_audit']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type_audit', 'status_job']
```

- `queryset` declares what I'll return. Here I return all the object with descending order of begin date
- `serializer_class` we use the Serializer we just created
- `ordering_fields` declares the fields on which we can order
- `filterset_fields` declares the fields on which we can filter

---
#### URLS

Now that we have all of that. How do we add it to our application.

You need to go to the root application and go to `urls.py`

```Python
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'api/extractor', ExtractorViewSet)
### Add your root here
router.register(r'api/<yourappName>', <NameofViewSet>)
```
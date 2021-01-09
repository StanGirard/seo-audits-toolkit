from django.contrib import admin

# Register your models here.

from .models import Yake

admin.site.register(Yake)

# Allows the Model to be administered via the /admin interface
# Highly recommendeded for easier debug
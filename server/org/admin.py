from django.contrib import admin

from .models import Website

admin.site.register(Website)

# Allows the Model to be administered via the /admin interface
# Highly recommendeded for easier debug
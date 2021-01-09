from django.contrib import admin

from .models import InternalLinks

admin.site.register(InternalLinks)
# Allows the Model to be administered via the /admin interface
# Highly recommendeded for easier debug
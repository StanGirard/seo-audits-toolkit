from django.contrib import admin

from .models import Extractor, Sitemap

admin.site.register(Extractor)
admin.site.register(Sitemap)

# Allows the Model to be administered via the /admin interface
# Highly recommendeded for easier debug
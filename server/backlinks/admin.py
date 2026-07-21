from django.contrib import admin

# Register your models here.

from .models import BacklinkAudit

admin.site.register(BacklinkAudit)

# Allows the Model to be administered via the /admin interface
# Highly recommended for easier debug

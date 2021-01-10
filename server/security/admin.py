from django.contrib import admin

from .models import Security, Security_Result

admin.site.register(Security)
admin.site.register(Security_Result)

# Allows the Model to be administered via the /admin interface
# Highly recommendeded for easier debug
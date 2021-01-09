from django.contrib import admin

from .models import Lighthouse, Lighthouse_Result

# Register your models here.


admin.site.register(Lighthouse)
admin.site.register(Lighthouse_Result)
# Allows the Model to be administered via the /admin interface
# Highly recommendeded for easier debug

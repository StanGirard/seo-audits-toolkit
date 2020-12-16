from django.contrib import admin

# Register your models here.

from .models import Lighthouse, Lighthouse_Result

admin.site.register(Lighthouse)
admin.site.register(Lighthouse_Result)
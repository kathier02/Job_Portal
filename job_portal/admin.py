from django.contrib import admin
from .models import Company, Job, Application

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
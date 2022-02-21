from django.contrib import admin
from .models import Project
from .models import Review,Tag

# Register your models here.

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

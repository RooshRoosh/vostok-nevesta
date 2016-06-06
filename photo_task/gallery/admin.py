from django.contrib import admin

# Register your models here.
from gallery.models import Image, Tag

admin.site.register(Image)
admin.site.register(Tag)
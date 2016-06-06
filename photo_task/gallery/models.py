from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField(max_length=512)
    create_at = models.DateTimeField()

    tags = models.ManyToManyField(Tag)

class Tag(models.Model):
    title = models.CharField(max_length=128)
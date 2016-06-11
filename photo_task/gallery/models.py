from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.conf import settings


def init_tag_cache():
    if not settings.TAGS_CACHE:
        settings.TAGS_CACHE = {i['title']: str(i['id']) for i in Tag.objects.values()}
    return settings.TAGS_CACHE


class Image(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField(max_length=512)
    create_at = models.DateTimeField()

    tags = models.ManyToManyField('Tag')
    likes = models.IntegerField(default=0)


class Tag(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

    def save(self, **kwargs):
        super(Tag, **kwargs)
        init_tag_cache()


class Like(models.Model):

    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
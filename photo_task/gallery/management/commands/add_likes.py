# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint, random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from gallery.models import Image, Like

class Command(BaseCommand):

    def handle(self, *args, **options):
        MAX_LIKE = 16
        user_list = {}
        user_count = User.objects.count()-1

        for image in Image.objects.all():
            like_count = randint(1, MAX_LIKE)
            for i in range(like_count):

                user_id = randint(1, user_count)

                if not user_list.get(user_id):
                    try:
                        user = User.objects.get(pk=user_id)
                    except:
                        continue
                    user_list[user_id] = user

                    Like.objects.create(
                        user=user,
                        image=image
                    )
                image.likes = like_count
                image.save()

            print(image.pk)
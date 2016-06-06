# -*- coding: utf-8 -*-
from datetime import datetime
import csv

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from gallery.models import Image#, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Создание пользователей

        users = {}
        with open('test-photo.csv') as f:
            reader = csv.reader(f, delimiter=';')
            reader.next()
            for (user_id, image_url, create_at) in reader:

                user = users.get(user_id)
                if not user:
                    user = User.objects.create_user(user_id, user_id+'@gmail.com', user_id*3)
                    users[user_id] = user

                Image.objects.create(
                    user=user,
                    url=image_url,
                    create_at=datetime.strptime(create_at, '%Y-%m-%d %H:%M:%S')
                )
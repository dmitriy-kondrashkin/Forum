from main.models import Post
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import random


class Command(BaseCommand):
    Post.objects.all().delete()

    def handle(self, *args, **options):
        posts = [Post(
            title=f'title of the post{index}', content=f'content of the post {index}', slug=f'la{get_random_string(length=15)}_{random.randint(100,10000)}') for index in range(1, 300)]
        Post.objects.bulk_create(posts)

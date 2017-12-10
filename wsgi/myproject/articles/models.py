from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Article(models.Model):
    source_name = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=300, blank=False)
    description = models.TextField(blank=False)
    image_url = models.TextField(blank=False)
    url = models.TextField(blank=False)
    published_at = models.DateTimeField()
    likes = models.ManyToManyField(CustomUser, blank=True)
    category = models.CharField(blank=False,max_length=30)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments')
    user = models.ForeignKey(CustomUser, related_name='commenter')
    text = models.TextField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=50)
    text = models.TextField()
    isProtected = models.BooleanField()
    postDate = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    postImage = models.ImageField(null=True, blank=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    commentDate = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def publish(self):
        self.commentDate = timezone.now()
        self.save()

    def __str__(self):
        return self.text


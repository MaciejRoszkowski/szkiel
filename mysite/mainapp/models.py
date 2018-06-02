from django.db import models

# Create your models here.


class Blog(models.Model):
    Name = models.CharField(max_length=100)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="none")
    text = models.TextField()
    passwd = models.CharField(max_length=10)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)


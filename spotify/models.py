from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Many to many: authors = models.ManyToManyField(User)
    # One to one: author = models.OneToOneField(User)

    class Meta:
        permissions = [
            ('change_post_content', 'Can change post content')
        ]

    def __str__(self):
        return f'{self.id}. {self.title}'


class JwtIdentifier(models.Model):
    identifier = models.CharField(max_length=255)

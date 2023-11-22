from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Repository(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=350, blank=True, null=True)
    url = models.URLField(unique=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    stars = models.IntegerField()
    issues = models.IntegerField()
    forks = models.IntegerField()
    last_commit = models.DateTimeField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_repositories = models.ManyToManyField('Repository', blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username

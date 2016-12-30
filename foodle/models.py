from django.db import models

# Create your models here.
class gn(models.Model):
    url = models.URLField('url', unique=True, primary_key=True)
    ind = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    subtitle = models.CharField(max_length=2048)
    data = models.CharField(max_length=1024)
    photo = models.CharField(max_length=1024)

    def __str__(self):
        return self.title

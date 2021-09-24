from django.db import models


class ImageModel(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')

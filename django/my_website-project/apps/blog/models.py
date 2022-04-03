from django.db import models


class BlogPost(models.Model):
    title = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=250
    )
    date = models.DateField(
        blank=True
    )
    post_text = models.TextField(
    )
    image = models.ImageField(
        upload_to='blog/images',
        blank=True
    )

    def __str__(self):
        return self.title

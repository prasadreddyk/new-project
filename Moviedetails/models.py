from django.db import models

# Create your models here.
class Movies(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    description = models.TextField(max_length=255)
    last_edited_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
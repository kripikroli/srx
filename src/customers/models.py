from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='customers', default='no_avatar.png')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)



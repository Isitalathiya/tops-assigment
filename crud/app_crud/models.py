from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50,null=True)
    email = models.EmailField(max_length=50,null=True)
    mobile = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.name 
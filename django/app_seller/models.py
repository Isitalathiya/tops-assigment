from django.db import models

# Create your models here.
class seller_User(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.fullname
    
        
    
class AProduct(models.Model):
    name=models.CharField(max_length=50)
    price=models.CharField(max_length=5)
    description=models.CharField(max_length=500)
    image=models.FileField(upload_to="media/",default="shaku")
    seller=models.ForeignKey(seller_User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

    



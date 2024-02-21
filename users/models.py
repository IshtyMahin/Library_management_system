from django.db import models

# Create your models here.
from django.contrib.auth.models import User

GENDER=(
    ('Male','Male'),
    ('Female','Female')
)

class UserAccount(models.Model):
    user  = models.OneToOneField(User, related_name="account",on_delete=models.CASCADE)
    birth_date = models.DateTimeField(null=True,blank=True)
    gender = models.CharField(max_length=10,choices=GENDER)
    balance = models.DecimalField(max_digits=12,default=0,decimal_places=2)
    
    def __str__(self) -> str:
        return str(self.user.first_name)
    
class UserAddress(models.Model):
    user = models.OneToOneField(User,related_name="address",on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return str(self.user.email)
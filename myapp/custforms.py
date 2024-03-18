from django import custforms
from django.contrib.auth.forms import UserCreationForm
from myapp import models
from myapp.models import User
class Customer(UserCreationForm):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    dob=models.DateField()
    gender=models.CharField(max_length=100)
    email=models.EmailField()
    contact_number=models.IntegerField()
    class Meta:
        model=User
        fields=['name','age','dob','gender','email','contact_number']
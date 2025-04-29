from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to login account
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    date_of_joining = models.DateField()
    is_active = models.BooleanField(default=True)
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.full_name

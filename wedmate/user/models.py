from django.db import models
from vendor.models import *

class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.user.username

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



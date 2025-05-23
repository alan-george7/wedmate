from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    business_type = models.CharField(max_length=50)
    place = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='vendor_profile_pics/')
    bio = models.TextField()
    budget = models.CharField(max_length=100)
    budget_int = models.IntegerField(null=True, blank=True)
    organization = models.CharField(max_length=100)

class VendorWorkPhoto(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='work_photos/')


class VendorPayment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField()
    event_location = models.CharField(max_length=255)
    details = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.name} - {self.vendor.name} ({self.status})"

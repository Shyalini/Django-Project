from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')

    def __str__(self):
        return self.user.username


class Package(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='package_images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    number_of_people = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Booking {self.pk} for {self.user.username}"

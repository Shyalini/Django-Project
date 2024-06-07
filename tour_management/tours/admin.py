from django.contrib import admin
from .models import Vendor, Package, Booking

# Register your models here.


admin.site.register(Vendor)
admin.site.register(Package)
admin.site.register(Booking)

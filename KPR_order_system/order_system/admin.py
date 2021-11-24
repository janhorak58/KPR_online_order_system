from django.contrib import admin
from .models import Order, Book, Shipping, Address

# Register your models here.

admin.site.register(Order)
admin.site.register(Book)
admin.site.register(Shipping)
admin.site.register(Address)

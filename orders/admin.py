from django.contrib import admin

from .models import Order
# Register your models here.

# class CartAdmin(admin.ModelAdmin):
#     class Meta:
#         model= Order

admin.site.register(Order)

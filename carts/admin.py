from django.contrib import admin

# Register your models here.


from .models import Cart,CartItem
# admin for the cart and accessible in the admin page
class CartAdmin(admin.ModelAdmin):
    class Meta:
        model= Cart

admin.site.register(Cart, CartAdmin)

admin.site.register(CartItem)
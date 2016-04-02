from django.contrib import admin
# Register your models here.
from .models import Product, ProductImage, Variation



#show more information about eaach instance in the admin page
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    ##adding the items to have a searchable characteristic
    search_fields = ['title', 'description']

    #fields in products/models.py
    list_display = ['title', 'price', 'active', 'updated']

    #give the admin the edit capabilities in the items
    list_editable = ['price', 'active']

    #Sorting out the list based on characteristics
    list_filter =  ['price', 'title']

    #these are the readonly fields
    readonly_fields = ['updated', 'timestamp']

    #prepopulating the slug field based on the title
    prepopulated_fields = {"slug":("title",)}

    class Meta:
        model = Product

#register the model to the admin.
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)

admin.site.register(Variation)


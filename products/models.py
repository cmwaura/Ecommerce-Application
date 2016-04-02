from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Product(models.Model):
    ##all of the item characteristics that we will add into the db##
    title = models.CharField(max_length=140, blank= False)
    description= models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits= 100, default=29.99, decimal_places= 2)
    sale_price = models.DecimalField(max_digits= 100, null=True, blank=True, decimal_places= 2)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title


    class Meta:
        unique_together = ("title", "slug")

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse("single_product", kwargs={"slug":self.slug})
        #return "/products/%s/"%(self.slug)

## the upcoming section is made possible after installing pillow to python. **check that//
## you have pillow or use pip to install it.
## creating an image field.
class ProductImage(models.Model):
    product= models.ForeignKey(Product)
    image = models.ImageField(upload_to= 'products/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.product.title
#setting up the variations manager for variations
# These are the models that are dedicated to all the different variations that a product would be

class VariationManager(models.Manager):
    #setting the active to true
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category="size")

    def color(self):
        return self.all().filter(category="color")

    def package(self):
        return self.all().filter(category="package")


# the tuples of different categories in the product variations.
VAR_CATEGORIES = (
    ("size", "size"),
    ("color", "color"),
    ("package", "package")

)
# creating the models for the product variations
class Variation(models.Model):
    # linking up the product variation to the product itself
    product= models.ForeignKey(Product)

    # all the categories expressed within the tuple VAR_CATEGORIES now placed in the model
    category= models.CharField(max_length=120, choices=VAR_CATEGORIES, default="color")

    # linking up the product variation to the product image.
    image= models.ForeignKey(ProductImage, null=True, blank=True)

    title = models.CharField(max_length=120)
    price= models.DecimalField(max_digits=100, decimal_places=2,null=True, blank=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    #setting up the variations manager so that the variations can work
    objects= VariationManager()


    def __unicode__(self):
       return self.title

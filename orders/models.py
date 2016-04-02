from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from carts.models import Cart

user = get_user_model()
# status choice for your order
STATUS_CHOICES= (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)


class Order(models.Model):
    user = models.ForeignKey(user,blank=True, null=True)
    order_id = models.CharField(max_length=120, default="ABC", unique=True)
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="started")
    sub_total= models. DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    tax_total= models. DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    final_total= models. DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.order_id
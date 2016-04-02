import time

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect


from orders.models import Order
from carts.models import Cart

from .utils import id_generator
# Create your views here.

def orders(request):
    context={}
    return render(request, "orders/user.html", context)

# the process of the end user checking out with their cart.
@login_required
def checkout(request):

    ## using the session we created during carts to collect the cart_id.
    try:
        the_id = request.session['cart_id']
        cart= Cart.objects.get(id= the_id)
        print cart
    except :
        the_id= None
    ## Redirects to a url that we had initially configured in django urls page
        return HttpResponseRedirect(reverse("cart"))

# Creating a new instance if there is no order present. This instance will be saved as the
# new order.
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
   # it will return the user back to the cart
    except:
        return HttpResponseRedirect(reverse("cart"))




   # If the order is indicated as finished the cart will be deleted as well as
    # resetting the total number of items back to zero.
    if new_order.status== "Finished":
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse("cart"))

    context={}
    return render(request, "products/home.html", context)
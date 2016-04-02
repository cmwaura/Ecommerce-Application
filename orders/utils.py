__author__ = 'crispus'

import string
import random
# from .models import Order
# generating an id to assign to each order in the checkout.size is 12 with upercase string
# and digits combination.
def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    the_id="".join(random.choice(chars) for x in range(size))
    print the_id
    # # If the order exist we will need to run the generator again to create a new order
    # # sequence. All order sequences must be unique.
    # try:
    #     #if it exists i.e order_id is the same as the_id run the id generator again.
    #     order = Order.objects.get(order_id = the_id)
    #     id_generator()
    # except Order.DoesNotExist:
    #     return the_id
id_generator()
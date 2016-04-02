import stripe
import random
import hashlib


from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save



from .models import UserStripe, EmailConfirmed

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

# If we decide to change how we need to add the stripe id this is where we set
# for a user_logged_in.

# def get_or_create_stripe(sender, user, *args,**kwargs):
#     # print sender
#     # print user.email
#     try:
#         user.userstripe.stripe_id
#     except UserStripe.DoesNotExist:
#         customer = stripe.Customer.create(
#             email = user.email
#
#         )
#         new_user_stripe = UserStripe.objects.create(
#             user = user,
#             stripe_id = customer.id
#         )
#     except:
#         pass


#sending in a user instance.
# user_logged_in.connect(get_or_create_stripe)

def get_create_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
        email = user.email
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()

def user_created(sender, instance, created, *args,**kwargs):
    user = instance
# create a new user and once created, it will get or create the user stripe then/
# it will email the user and activation code.
    if created:
        get_create_stripe(user)
        email_confirmed, email_is_created= EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random())).hexdigest()
            username, domain = str(user.email).split('@')
            activationkey = hashlib.sha1(short_hash+username).hexdigest()
            email_confirmed.activationkey = activationkey
            email_confirmed.save()
            email_confirmed.activate_user_email()

post_save.connect(user_created, sender=User)




from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models

from django.template.loader import render_to_string
# Create your models here.


class UserStripe(models.Model):
    # incase we ever want a custom user model the model below would help
    # in changing it on the fly
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=120, null= True, blank= True)

    def __unicode__(self):
        return str(self.stripe_id)

# Sending an email to confirm your new account. The email will contain an activation
# key that once activated will create and save then user account
class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    activationkey = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        # activate the url by sending it to the site url and through reverse we sent it to the activation
        # module thereby accessing the activation key which is set as the argument.
        activation_url = "%s%s" %(settings.SITE_URL, reverse("activation_view",args=[self.activationkey]))
        context= {
            "activationkey":self.activationkey,
            "activation_url": activation_url,
            "user": self.user.username,
        }
        # The message that would be rendered/sent to the first time user who is trying to
        # create and account.
        message = render_to_string("accounts/activation_message.txt", context)

        subject = 'Activate Your Account'
        print message
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

        #send email here and render a string
        # user.emailedconfirmed.email_user()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)
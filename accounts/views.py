import re
from django.shortcuts import render,HttpResponseRedirect, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.urlresolvers import reverse


from .forms import LoginForm, RegistrationForm
from .models import EmailConfirmed
# Create your views here.


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logged out. Please <a href='%s'>login</a> to continue your experience."%(reverse("auth_login")), extra_tags='safe')
    # messages.warning(request, "this is warning")
    # messages.error(request, "there is an error!")
    return HttpResponseRedirect('/')

def login_view(request):
# Importing the form for login from forms.py and then issuing that it will take
# the post data or take no data at all.

    form  = LoginForm(request.POST or None)
    btn = "Login"
# Check the validation of the data you enter in the form
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        # user.emailconfirmed.activate_user_email()
        messages.success(request, "Welcome back " + str(username) +" You are successfully logged in.")
        # next_url = request.GET.get('next', None)
        #  print next_url
        # if next_url is not None:
        #     return HttpResponseRedirect(next_url)
        return HttpResponseRedirect("/")

    context= {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "form.html", context)



def registration_view(request):
# Importing the form for register from forms.py and then issuing that it will take
# the post data or take no data at all.

    form  = RegistrationForm(request.POST or None)
    btn = "Register"
# Check the validation of the data you enter in the form
    if form.is_valid():

        new_user= form.save(commit=False)
        # new_user.first_name= "cris" where you can customize the model
        new_user.save()
        # this will redirect the user to the page he should be going to
        messages.success(request, "Successfully Registered. Please confirm your email now.")
        return HttpResponseRedirect("/")
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request, user)

    context= {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "form.html", context)


SHA1_RE = re.compile('^[a-f0-9]{40}$')

def activation_view(request, activationkey):
    if SHA1_RE.search(activationkey):
        print "activation key is real"
        try:
            instance = EmailConfirmed.objects.get(activationkey=activationkey)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "There was an error with your request.")
            return HttpResponseRedirect("/")

            # raise Http404
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation successful! Welcome"
            instance.confirmed = True
            instance.activationkey = "Confirmed"
            instance.save()
            messages.success(request, "Successfully Confirmed.Please Login")
        elif instance is not None and instance.confirmed:
            page_message = "User already confirmed"
        else:
            page_message = ""


        context = {"page_message":page_message}
        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404
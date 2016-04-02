from django.shortcuts import render, Http404

from .models import Product, ProductImage
from marketing.models import MarketingMessage

# Create your views here.

#home page with all the products that the admin will add.
def home(request):
    products = Product.objects.all()
    # marketing_message = MarketingMessage.objects.all()[0]
    context = {'products':products}

    return render(request, "products/home.html", context)

#the search button queries the results of what you search.
def search(request):
    try:
       q = request.GET.get('q')
    except:
        q = None
    if q:
        products =Product.objects.filter(title__icontains=q)
        context = {"query":q, 'products':products}
        template = "products/results.html"
    else:
        context = {}
        template = "products/home.html"
    return render(request, template, context)


def all(request):
    # del request.session['marketing_message']
    #grabbing all the objects in the products module by models.py
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "products/all.html", context)


def single(request, slug):

    try:
        #grabbing all the objects in the products module by models.py
        product = Product.objects.get(slug=slug)
        #images = product.productimages_set.all()
        images =ProductImage.objects.filter(product=product)
        # products = Product.objects.all()
        context = {'product':product, "images": images}
        return render(request, "products/single.html", context)
    except:
        raise Http404
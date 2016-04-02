from django.conf.urls import patterns, include, url
from django.contrib import admin
# for the static files
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Url for products
     url(r'^$', 'products.views.home', name='home'),
     url(r'^products/$', 'products.views.all', name='products'),
     url(r'^s/$', 'products.views.search', name='search'),
     url(r'^products/(?P<slug>[\w-]+)/$', 'products.views.single', name='single_product'),

     #urls that are for the  cart
     url(r'^cart/$', 'carts.views.view', name='cart'),
     url(r'^cart/(?P<id>\d+)/$', 'carts.views.remove_from_cart', name='remove_from_cart'),
     url(r'^cart/(?P<slug>[\w-]+)/$', 'carts.views.add_to_cart', name='add_to_cart'),

        #urls that are for orders
     url(r'^checkout/$', 'orders.views.checkout', name='checkout'),
     url(r'^orders/$', 'orders.views.orders', name='user_orders'),


     url(r'^admin/', include(admin.site.urls)),
     url(r'^accounts/logout/$','accounts.views.logout_view', name='auth_logout'),
     url(r'^accounts/login/$','accounts.views.login_view', name='auth_login'),
     url(r'^accounts/register/$','accounts.views.registration_view', name='auth_register'),
     url(r'^accounts/activate/(?P<activationkey>\w+)/$', 'accounts.views.activation_view', name='activation_view'),


)
# if the Debug settings is true then it will serve the static and media files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
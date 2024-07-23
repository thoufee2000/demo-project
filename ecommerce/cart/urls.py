"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views



from django.conf.urls.static import static

app_name='cart'
urlpatterns = [

    path('cart/<int:i>',views.add_to_cart,name='add_to_cart'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('remove/<int:i>/<int:c_id>',views.cart_remove,name='remove'),
    path('decrement/<int:i>',views.decrement,name='decrement'),
    path('place_order',views.place_order,name='place_order'),
    path('status/<u>',views.payment_status,name='payment_status'),
    path('orders/',views.order_details,name='orders'),

]

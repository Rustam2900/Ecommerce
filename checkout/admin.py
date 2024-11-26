from django.contrib import admin
from .models import CheckoutBasket, BillingDetails, ProductCheckout

admin.site.register(CheckoutBasket)
admin.site.register(ProductCheckout)
admin.site.register(BillingDetails)

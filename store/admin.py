from django.contrib import admin
from .models import Product, OrderProduct, Order, CheckoutAddress, Device, Theme


admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Device)
admin.site.register(Theme)
admin.site.register(CheckoutAddress)
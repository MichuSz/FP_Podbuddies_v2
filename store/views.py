from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils import timezone
from .models import Product, Order, OrderProduct


class HomeView(ListView):
    model = Product
    template_name = "home.html"

class ProductView(DetailView):
    model = Product
    template_name = "product.html"

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk = pk)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request,"Quantity changed.")
            return redirect("store:product",pk=pk)
        else:
            order.products.add(order_product)
            messages.info(request,"Product added to your shopping cart.")
            return redirect("store:product",pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request,"Product added to your shopping cart.")
        return redirect("store:product",pk=pk)

def remove_from_cart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order_product = order_qs[0]
        if order.products.filter(product__pk=item.pk).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            order_product.delete()
            messages.info(request, f"Item {order_product.product.product_name} remove from your cart")
            return redirect("store:product")
        else:
            messages.info(request, "You dont have that product in your bucket.")
            return redirect("store:product",pk=pk)
    else:
        messages.info(request, "You dont even have an order.")
        return redirect("store:product", pk=pk)
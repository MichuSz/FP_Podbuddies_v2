from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils import timezone
from .models import Product, Order, OrderProduct, CheckoutAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm


class HomeView(ListView):
    model = Product
    template_name = "home.html"


class ProductView(DetailView):
    model = Product
    template_name = "product.html"


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'order_summary.html', { 'object' : order })
        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an order.")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        return render(self.request, 'checkout.html',{'form':form})

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_adress = form.cleaned_data.get('same_billing_adress')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_adress = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_adress.save()
                order.checkout_adress = checkout_adress
                order.save()
                return redirect('store:checkout')
            messages.warning(self.request,"Failed checkout.")
            return redirect('store:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an order.")
            return redirect('store:order-summary')

@login_required
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
            return redirect("store:order-summary")
        else:
            order.products.add(order_product)
            messages.info(request,"Product added to your shopping cart.")
            return redirect("store:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request,"Product added to your shopping cart.")
        return redirect("store:order-summary")

@login_required
def remove_from_cart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            order_product.delete()
            messages.info(request, f"Item {order_product.product.product_name} remove from your cart")
            return redirect("store:order-summary")
        else:
            messages.info(request, "You dont have that product in your bucket.")
            return redirect("store:product",pk=pk)
    else:
        messages.info(request, "You dont even have an order.")
        return redirect("store:product", pk=pk)

@login_required
def reduce_quantity_product(request,pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order_product.delete()
            messages.info(request, "Product quantity updated.")
            return redirect("store:order-summary")
        else:
            messages.info(request, "This thing is not in your cart.")
            return redirect("store:order-summary")
    else:
        messages.info(request, "You need an Order to do that.")
        return redirect("store:order-summary")



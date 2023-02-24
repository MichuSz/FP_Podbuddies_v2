from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils import timezone
from .models import Product, Order, OrderProduct, CheckoutAddress, Payment, LABEL, Device, Theme
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from django.conf import settings


import stripe
stripe.api_key = settings.STRIPE_KEY

label = LABEL


class HomeView(ListView):
    model = Product
    template_name = "home.html"
    paginate_by =15

class ProductView(DetailView):
    model = Product
    template_name = "product.html"


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'order_summary.html', {'object' : order })
        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an order.")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user,ordered=False)
        return render(self.request, 'checkout.html', {'form':form,'order':order})

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
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

                if payment_option == 'S':
                    return redirect('store:payment',payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('store:payment',payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid payment option")
                    return redirect('store:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an order.")
            return redirect('store:order-summary')

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        return render(self.request, "payment.html", {'order': order})

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        #token = self.request.POST.get('stripeToken')
        amount = int(order.get_total_price()*100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="pln",
                source="tok_mastercard"
            )

            # create payment
            payment = Payment()
            payment.stripe_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_price()
            payment.save()

            # assign payment to order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Successfully made an order")
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('/')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "To many request error")
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid Parameter")
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Authentication with stripe failed")
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect('/')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect('/')

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "Not identified error")
            return redirect('/')





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


def category_list(request,id=Device.pk):
    devices = Device.objects.all().order_by('id')
    products = Product.objects.filter(device=id)
    themes = Theme.objects.all().order_by('id')
    return render(request,'category_list.html',{'devices':devices,'products':products,'themes':themes})


def theme_list(request,id=Theme.pk):
    themes = Theme.objects.all().order_by('id')
    devices = Device.objects.all().order_by('id')
    products = Product.objects.filter(theme=id)
    return render(request,'theme_list.html',{'themes':themes,'products':products,'devices':devices})




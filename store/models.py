from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY = (
    ('AP12', 'Apple AirPods 1&2'),
    ('AP3', 'Apple AirPod Pro'),
    ('AD12', 'Xiaomi AirDots 1&2'),
    ('AD3', 'Xiaomi AirDots 3'),
)

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller')
)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY, max_length=4)
    label = models.CharField(choices=LABEL, max_length=2)
    description = models.TextField()

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):  # return url from product
        return reverse("store:product", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):  # return url to function add item to cart
        return reverse("store:add-to-cart", kwargs={"pk": self.pk})

    def get_remove_cart_url(self):  # return url to function remove item from cart
        return reverse("store:remove-from-cart", kwargs={"pk": self.pk})


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_discount_product_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_discount_product_price()
        return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total

class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
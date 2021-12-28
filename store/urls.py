from django.urls import path
from .views import remove_from_cart, add_to_cart,reduce_quantity_product,OrderSummaryView, ProductView, HomeView, CheckoutView


app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<pk>', ProductView.as_view(),name='product'),
    path('add-to-cart/<pk>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>', remove_from_cart, name='remove-from-cart'),
    path('order-summary', OrderSummaryView.as_view(), name='order-summary'),
    path('reduce-quantity-product/<pk>', reduce_quantity_product, name='reduce-quantity-product'),
    path('checkout/',CheckoutView.as_view(),name='checkout')

]
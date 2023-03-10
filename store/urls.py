from django.urls import path

from . import views
from .views import remove_from_cart, add_to_cart, reduce_quantity_product, OrderSummaryView, ProductView, HomeView, CheckoutView, PaymentView


app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<pk>', ProductView.as_view(),name='product'),
    path('add-to-cart/<pk>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>', remove_from_cart, name ='remove-from-cart'),
    path('order-summary', OrderSummaryView.as_view(), name='order-summary'),
    path('reduce-quantity-product/<pk>', reduce_quantity_product, name='reduce-quantity-product'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment'),
    path('category-list/<int:id>/', views.category_list,name='category-list'),
    path('theme-list/<int:id>/', views.theme_list,name='theme-list')
    # path('category/<pk>',DeviceView.as_view(),name='device-type')
]



from store.models import Device,Theme,Product
import pytest

@pytest.mark.django_db
def test_create_device():
    device = Device.objects.create(device="Sony X32 Plug")
    assert device.device == "Sony X32 Plug"

@pytest.mark.django_db
def test_create_theme():
    theme = Theme.objects.create(theme="Fancy Color")
    assert theme.theme == "Fancy Color"

# @pytest.mark.django_db
# def test_create_product():
#     product = Product.objects.create(product_name="Awsomeness",
#                                      price= 15,
#                                      discount_price =10,
#                                      label="bs",
#                                      description="This is random text",
#                                      img="4.jpg",
#                                      device_id=1,
#                                      theme_id=4)
#
#     assert product.product_name == "Awsomeness"
#     assert product.price == 15
#     assert product.discount_price == 10
#     assert product.label == "bs"
#     assert product.description == "This is random text"
#     assert product.img == "4.jpg"
#     assert product.device_id == 1
#     assert product.theme_id == 4


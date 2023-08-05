from django import forms
from django.forms import ModelForm
from .models import  Order,Order_item_model,order_items_menu,Checkout_order

class Quantity_update(ModelForm):

    class Meta:
        model=Order_item_model
        fields = ["item_quantity"]

class Size_update(ModelForm):

    class Meta:
        model=order_items_menu
        fields = ["item_size"]
class Checkout_order_form(ModelForm):
    class Meta:
        model=Checkout_order
        fields="__all__"
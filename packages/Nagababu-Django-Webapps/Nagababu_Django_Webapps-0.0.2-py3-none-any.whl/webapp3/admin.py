from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import order_items_menu,Order_item_model,Order,Checkout_order
# Register your models here.
admin.site.register(order_items_menu)
admin.site.register(Order_item_model)
admin.site.register(Order)
admin.site.register(Checkout_order)




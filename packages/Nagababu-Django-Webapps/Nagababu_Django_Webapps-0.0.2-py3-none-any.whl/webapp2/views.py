from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Page_Nav_Items,Page_Items,Cuisine
from webapp3.models import order_items_menu,Order,Order_item_model
# Create your views here.
# login_required(login_url="/food/Login/")
def home(request):
    if request.user.is_authenticated:
        model=Page_Nav_Items.objects.all()
        item_data=Page_Items.objects.all()
        cu_data=Cuisine.objects.all()
        all_items = Order_item_model.objects.filter(user=request.user)
        # order_items_data = order_items_menu.objects.all()
        # num_of_orders=Order_item_model.objects.count()
        num_of_orders=len(all_items)
        total_cost=0
        for i in all_items:
            total_cost+=i.item_price*i.item_quantity

        return  render(request,'webapp2/home.html',{"num_of_orders":num_of_orders,"page_items":model,"item_data":item_data,"cu_data":cu_data,"all_items":all_items,"Total_cost":total_cost})
    else:
        return redirect('Login')
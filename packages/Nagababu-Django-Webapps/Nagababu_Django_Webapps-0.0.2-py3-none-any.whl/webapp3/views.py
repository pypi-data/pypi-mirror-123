from django.shortcuts import render,redirect
import razorpay
from django.http import JsonResponse

from django.conf import  settings
from django.http import HttpResponse
from django.views import View
from .models import order_items_menu,Order_item_model,Order
from django.views import generic
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import  Quantity_update,Size_update,Checkout_order_form
# Create your views here.
from django.contrib.auth.decorators import login_required
# login_required(login_url="food/Login/")
# total_cost=0
def home(request):
    # form_size=Size_update()
    if request.user.is_authenticated:
        order_items_data=order_items_menu.objects.all()
        all_items = Order_item_model.objects.filter(user=request.user)
        # total_orders=Order_item_model.objects.count()
        total_orders=len(all_items)
        # global total_cost
        total_cost=0
        for i in all_items:
            total_cost +=i.total_price
        total_cost=("%.2f"% total_cost)
        return render(request,'webapp3/home_items.html',{"order_items_data":order_items_data, "all_items":all_items,"num_of_orders":total_orders,"Total_cost":total_cost})

    else:
        return redirect('webapp1:Login')

# class Indexview(generic.ListView):
#     model=order_items_menu
#     template_name = "webapp32/home_items.html"
#     def Ret(self):
#         return  order_items_menu.objects.all()
#{% for i in object_list %}
#
def OrderView(request,slug):
    item=get_object_or_404(order_items_menu,slug=slug)

    order_item,created=Order_item_model.objects.get_or_create(item=item,user=request.user,item_image=item.item_image,item_title=item.item_title,item_price=item.item_cost,slug=slug,total_price=item.item_cost)
    order_qr=Order.objects.filter(user=request.user,ordered=False)
    if order_qr.exists():  # if the user logged then request.user contains the currently logged user
        order=order_qr[0]   # Ex: <Order:["Nagababu"]
        if order.items.filter(item__slug=item.slug).exists():
        # if order.items.filter(item__slug=item.slug).exists():
            order_item.item_quantity+=1
            order_item.total_price+=order_item.item_price
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        t=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=t)
        order.items.add(order_item)
    all_items = Order_item_model.objects.filter(user=request.user)
    order_items_data = order_items_menu.objects.all()
    # total_orders = Order_item_model.objects.count()
    total_orders=len(all_items)
    total_cost = 0
    for i in all_items:
        total_cost = i.item_price * i.item_quantity
    #return render(request,'webapp3/home_items.html',{"Total_cost":total_cost,"all_items":all_items,"user":request.user,"order_items_data": order_items_data,"num_of_orders":total_orders})
    return  redirect("webapp3:home")


def deleteview(request,slug):
    item=get_object_or_404(order_items_menu,slug=slug)  # clicked item in order_items_menu
    cart_order_item=Order_item_model.objects.filter(item=item)
    if cart_order_item.exists():
        cart_order_item.delete()
        return  redirect("webapp3:home")
    else:
        return HttpResponse("Please try again")



def displaty_cart(request):

    form=Quantity_update()
    all_items_cart = Order_item_model.objects.filter(user=request.user)
    num_of_orders=len(all_items_cart)
    total_cost = 0
    for i in all_items_cart:
        total_cost += i.total_price
    return render(request,'webapp3/cart.html',{"form":form,"all_items":all_items_cart,"num_of_orders":num_of_orders,"Total_cost":total_cost})


def Checkout(request):
    if request.method == "POST":
        filled_login_form = Checkout_order_form(request.POST)

        if filled_login_form.is_valid():
            name=filled_login_form.cleaned_data['your_name']
            number=filled_login_form.cleaned_data["mobile_no"]
            delivery = filled_login_form.cleaned_data["delivery_time"]
            order_type = filled_login_form.cleaned_data["type_of_order"]
            order_city = filled_login_form.cleaned_data["city"]
            address=filled_login_form.cleaned_data["address"]
            payment_type = filled_login_form.cleaned_data["payment_type"]
            print(name,number,delivery,order_city,order_type,payment_type)
            ###### RAZORPAY *********************

            ###final user cost
            all_items = Order_item_model.objects.filter(user=request.user)
            # num_of_orders=Order_item_model.objects.count()
            num_of_orders = len(all_items)

            delivery_tax = 6
            total_cost = 0
            for i in all_items:
                total_cost += i.total_price
            final_cost = "%.2f" % (total_cost + delivery_tax)


            order_amount = 100
            # return render(request,"webapp3/check.html",{"st":order_amount})
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'
            client = razorpay.Client(auth=('rzp_test_ZEXJEXEsfgAtHm','2U8nm25ArSO4113rkuEhbyuc'))
            payment_order = client.order.create(
               {"amount":order_amount, "currency":order_currency, "receipt":order_receipt, "payment_capture":1,
                })

            payment_order_id = payment_order['id']

            #########
            cleaned_form=Checkout_order_form()

            if payment_type=="Pay with cash to the courier":
                return HttpResponse("Order received")
            else:
                return render(request,"webapp3/bill.html",{

                    "amount":order_amount,"api_key":"rzp_test_ZEXJEXEsfgAtHm","order_id":payment_order_id,"mobile":number,"email":request.user.email,"name":name})

    form=Checkout_order_form()
    all_items = Order_item_model.objects.filter(user=request.user)
    # num_of_orders=Order_item_model.objects.count()
    num_of_orders=len(all_items)

    delivery_tax=6
    total_cost = 0
    for i in all_items:
        total_cost += i.total_price
    final_cost="%.2f"%(total_cost+delivery_tax)



    if total_cost==0:
        return render(request, 'webapp3/checkout.html',
                      {"all_items": all_items, "num_of_orders": num_of_orders, "Total_cost":0.0,
                       "Delivery_tax":0.0,"Final_cost":0.0 , "form_check":form})
    else:

        return render(request,'webapp3/checkout.html',{"form_check":form,"all_items":all_items,"num_of_orders":num_of_orders,"Total_cost":total_cost,"Delivery_tax":delivery_tax,"Final_cost":final_cost})

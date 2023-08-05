from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.

#size = forms.ChoiceField(label='Size', choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
Size_CHOICES = [
    ('small', 'Small'),
    ('medium', 'Medium.'),
    ('standard', 'Standars'),
    ('large', 'Large'),
    ('thin','Thin'),
]

class order_items_menu(models.Model):
    item_image=models.ImageField(upload_to='order_menu_page/')
    item_title=models.CharField(max_length=100)
    item_desc=models.CharField(max_length=100)
    item_size=models.CharField(max_length=20,choices=Size_CHOICES,default="select")
    item_cost=models.FloatField(default=0)
    slug=models.SlugField()
    def __str__(self):
        return self.item_title
# class Duummy(models.Model):
#     img=models.ImageField(upload_to='naga/')
#     title=models.CharField(max_length=100)
#     desc=models.CharField(max_length=100)
#     slug=models.SlugField()
#     def __str__(self):
#         return self.title

    def get_absolute_url(self):
        return  reverse("webapp3:order",kwargs={
            'slug':self.slug
        })

class Order_item_model(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item=models.ForeignKey(order_items_menu,on_delete=models.CASCADE)
    item_image=models.ImageField(upload_to="images_app2/")
    item_title=models.CharField(max_length=100)
    item_price=models.FloatField(default=0)
    item_quantity=models.IntegerField(default=1)
    total_price=models.FloatField(default=0)
    slug=models.SlugField()

    def __str__(self):
        return self.item_title
    def get_absolute_url_delete(self):
        return reverse("webapp3:delete",kwargs={
            'slug':self.slug

        })
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(Order_item_model)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

Delivery_Time = [('by11', 'by 11.00 AM'),('by11.15', 'by 11.00 AM'),('by11.30', 'by 11.30 AM'),('by11.45', 'by 11.45 AM'),('by12.00',']by 12.00 PM'),('by12.15', 'by 12.15 PM'),('by12.30', 'by 12.30 PM'),('by12.45', 'by 12.45 PM'),('by1.00', 'by 1.00  PM'),

]

cities=[ ('bapatla', 'Bapatla'),('charala', 'Chirala'),('guntur', 'Guntur'), ('ongole', 'Ongole'), ('nellore','Nellore'),
]
type_of_order=[("Hand it to me","Hand it to me"), ("Leave it at my door","Leave it at my door")]

payment_method=[('Pay with cash to the courier','Pay with cash to the courier'),('Online payment','Online Payment')]
class Checkout_order(models.Model):
    your_name=models.CharField(max_length=100)
    mobile_no=models.CharField(max_length=10)
    delivery_time=models.CharField(choices=Delivery_Time,max_length=100)
    # delivery_time =forms.CharField(label="", choices=Delivery_Time)
    type_of_order=models.CharField(choices=type_of_order,max_length=100)
    city=models.CharField(choices=cities,max_length=100)
    address=models.CharField(max_length=100)
    payment_type=models.CharField(choices=payment_method,max_length=100)


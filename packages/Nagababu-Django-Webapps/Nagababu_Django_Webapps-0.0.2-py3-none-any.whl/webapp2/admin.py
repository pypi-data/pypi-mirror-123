from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Page_Nav_Items,Page_Items,Cuisine
admin.site.register(Page_Nav_Items)
admin.site.register(Page_Items)

admin.site.register(Cuisine)

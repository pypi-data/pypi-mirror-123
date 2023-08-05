from django.db import models

class Page_Nav_Items(models.Model):
    item_pic=models.FileField(upload_to='page_nav/')
    item_text=models.CharField(max_length=100)
    def __str__(self):
        return self.item_text

class Page_Items(models.Model):
    item_cost=models.FloatField()
    item_image=models.ImageField(upload_to='page_items_image/')
    item_logo=models.ImageField(upload_to='page_items_logo/')
    logo_desc=models.CharField(max_length=100)
    item_desc=models.CharField(max_length=100)
    def __str__(self):
        return self.item_desc
class Cuisine(models.Model):
    cu_img=models.FileField(upload_to='cuisine/')
    cu_desc=models.CharField(max_length=100)
    def __str__(self):
        return self.cu_desc

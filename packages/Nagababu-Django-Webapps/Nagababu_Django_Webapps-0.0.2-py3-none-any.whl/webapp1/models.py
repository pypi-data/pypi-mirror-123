from django.db import models


class Items(models.Model):
    item_pic=models.ImageField(upload_to="images/")
    item_desc=models.CharField(max_length=30)
    def __str__(self):
        return self.item_desc
class PtCf_data(models.Model):
    pat=models.ImageField(upload_to="pc_data/")
    head=models.CharField(max_length=100)
    desc=models.CharField(max_length=100)
    link_text=models.CharField(max_length=100)

    def __str__(self):
        return self.head
class Top_rest(models.Model):
    top_img=models.ImageField(upload_to="to_rest/")

class Cusine(models.Model):
    cu_pic=models.FileField(upload_to='uploads/')
    cu_desc=models.CharField(max_length=100)
    def __str__(self):
        return self.cu_desc

class Hash(models.Model):
    user_email=models.EmailField(verbose_name="hash email",unique=True)
    user_hash_key=models.CharField(verbose_name="hash key" ,max_length=64)
    def __str__(self):
        return self.user_email
class Login_Model(models.Model):
    username=models.EmailField()
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.username

class Project_Ideas(models.Model):
    pro_title=models.CharField(max_length=10000)
    pro_email=models.EmailField()
    pro_description=models.TextField()
    pro_status=models.CharField(max_length=10000,default="",blank=True)
    def __str__(self):
        return self.pro_email
from django.contrib import admin
from .models import Items,Project_Ideas,Top_rest,PtCf_data
from  django.contrib.auth.models import User
from .forms import  CustRegiForm
# Register your models here.
class CustRegiAdmin(admin.ModelAdmin):
    fields = ["username","email","password"]
    list_display = ["username","email","is_active","is_staff"]
    add_form=CustRegiForm


admin.site.register(Items)
admin.site.register(Project_Ideas)
admin.site.register(Top_rest)
admin.site.register(PtCf_data)
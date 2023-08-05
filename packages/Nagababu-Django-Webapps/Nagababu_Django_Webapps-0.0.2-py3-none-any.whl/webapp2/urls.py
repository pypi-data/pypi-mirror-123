from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name="webapp2"
urlpatterns = [

   path('',views.home,name="home"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

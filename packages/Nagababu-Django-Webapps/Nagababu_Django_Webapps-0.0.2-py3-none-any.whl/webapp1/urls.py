from . import views
from django.conf import settings
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as v1

urlpatterns = [


    path('Registration/',views.Registration,name="Registration"),
    path('Login/',views.Login_func,name="Login"),

    path('password_change/',v1.PasswordChangeView.as_view(template_name="webapp1/password_change.html"),name="Password_change"),
    path('password_change_done/', v1.PasswordChangeDoneView.as_view(template_name="webapp1/password_change_complete.html"), name="password_change_done"),

    path('password_reset/',v1.PasswordResetView.as_view(template_name="webapp1/password_reset.html"), name="reset_password"),
    path('password_reset_confirm/<uidb64>/<token>/',v1.PasswordResetConfirmView.as_view(template_name="webapp1/password_reset_confirm.html"),name="password_reset_confirm"),
    path('password_reset_done',v1.PasswordResetDoneView.as_view(template_name='webapp1/password_reset_done.html'),name="password_reset_done"),

    path('password_reset_complete/', v1.PasswordResetCompleteView.as_view(template_name="webapp1/password_reset_complete.html"),name="password_reset_complete"),
    path('logout/',views.logoutview,name="logout"),
    path('Project/',views.Project_form_view,name="Project_idea"),
    path('update_profile/',views.UpdateView,name="update_profile"),
    path('activate/<uidb64>/<token>/',views.ActivateView, name='activate'),

    path('ideas/', views.Pro_Indexview, name="pro_list"),
    path('idea/<int:pk>/',views.Project_statusView,name="pro_status")


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


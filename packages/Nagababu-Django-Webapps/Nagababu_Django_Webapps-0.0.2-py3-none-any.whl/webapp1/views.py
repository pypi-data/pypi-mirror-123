import time
import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Items,PtCf_data,Top_rest,Cusine,Hash,Login_Model,Project_Ideas,Project_Ideas
from .forms import  CustRegiForm,Login_form, Hash_form,Project_form,update_profile
from django.contrib import messages
from  django.db.models import Q
from django.core.mail import send_mail,EmailMessage
import hashlib
from django.conf import settings
from django.contrib.auth import logout,login,authenticate
from  django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from webapp3.models import order_items_menu,Order,Order_item_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import  render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.utils.encoding import force_bytes,force_text
from django.contrib import messages
from django.views import generic
import  django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()
def home(request):
    all_items_data=Items.objects.all()
    pc=PtCf_data.objects.all()
    top=Top_rest.objects.all()
    cu=Cusine.objects.all()

    return render(request,'webapp1/home.html',{"all_items":all_items_data , "pc_data":pc,"Top":top,"cu":cu})

def Registration(request):

    if request.method=="POST":

                filled_reg_form=CustRegiForm(request.POST)
                try:
                    if filled_reg_form.is_valid():

                        reg_username = filled_reg_form.cleaned_data["username"]
                        reg_email = filled_reg_form.cleaned_data["email"]
                        password1 = filled_reg_form.cleaned_data["password1"]
                        password2 = filled_reg_form.cleaned_data["password2"]
                        print(reg_username,reg_email,password2,password1)


                        try:
                            res=User.objects.get(Q(email=reg_email))
                            if res.is_active:
                                messages.warning(request,"Email is already existed")
                                form = CustRegiForm()
                                return render(request, 'webapp1/status1.html', {"Registration_form": form})
                            else:
                                if password1!=password2:
                                    messages.error("password and confirmation password didn't matched")
                                    form = CustRegiForm()
                                    return render(request,"webapp1/status1.html",{"status": form})
                                else:
                                    res.delete()
                                    user = filled_reg_form.save(commit=False)
                                    user.is_active = False
                                    user=filled_reg_form.save(commit=False)
                                    user.is_active=False
                                    user.save()

                                    current_site=get_current_site(request)  # it returns the current site like 127.0.0.1
                                    mail_subject = 'Activate your Nsoft account.'
                                    from_email_user = settings.EMAIL_HOST_USER
                                 ## This is the emial body
                                    mail_messages=render_to_string('webapp1/reg_email.html',
                                                           {
                                                               'user': user,
                                                               'domain': current_site.domain,
                                                              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                              'token': account_activation_token.make_token(user),
                                                          })
                                    receiver=filled_reg_form.cleaned_data["email"]
                                    try:
                                        send_mail(mail_subject,mail_messages,from_email_user,[receiver])
                                        messages.info(request,'please go to your email and confirm then logged back')
                                        return render(request,'webapp1/confirm_notify.html')
                                    except:
                                        form = CustRegiForm()
                                        messages.error(request,"Please check your internet connection")
                                        return render(request, 'webapp1/status1.html', {"Registration_form": form})

                        except User.DoesNotExist:
                                user = filled_reg_form.save(commit=False)
                                user.is_active = False
                                user.save()
                                current_site = get_current_site(request)  # it returns the current site like 127.0.0.1
                                mail_subject = 'Activate your Nsoft account.'
                                from_email_user = settings.EMAIL_HOST_USER
                                ## This is the emial body
                                mail_messages = render_to_string('webapp1/reg_email.html',
                                                                 {
                                                                     'user': user,
                                                                     'domain': current_site.domain,
                                                                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                                                     'token': account_activation_token.make_token(user),
                                                                 })
                                receiver = filled_reg_form.cleaned_data["email"]
                                try:
                                    send_mail(mail_subject, mail_messages, from_email_user, [receiver])
                                    messages.error(request, 'please go to your email and confirm then logged back')
                                    return render(request, 'webapp1/confirm_notify.html')
                                except:
                                    form = CustRegiForm()
                                    messages.info(request, "Please check your internet connection")

                                    return render(request, 'webapp1/status1.html', {"Registration_form": form})
                    else:
                        messages.error(request,"This will be happend either one failed \n 1.username must be unique\n2.password and confirm password mismatch ")
                        return render(request,"webapp1/status.html")
                except Exception:
                    messages.info(request,"oops please try again!!!")
                    return render(request, "webapp1/status1.html")

    form=CustRegiForm()
    return  render(request,'webapp1/Registration.html',{"Registration_form":form})

def ActivateView(request,uidb64,token):

    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        messages.info(request,"Session was Experied")
        return render(request,"webapp1/status.html")
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        current_site = get_current_site(request)
        subject="Registration successful at Nsoft"
        mail_body=render_to_string('webapp1/reg_success.html',
                                   {'user':user,
                                    'domain': current_site.domain
                                    }
                                   )
        sender=settings.EMAIL_HOST_USER
        receiver=request.user.email
        try:
            send_mail(subject,mail_body,sender,[receiver])
        except:
            return ""
        return redirect('/')

def Login_func(request):
    if request.method=="POST":
        filled_login_form=Login_form(request.POST)

        if filled_login_form.is_valid():

            login_email=filled_login_form.cleaned_data["Email"]
            login_password=filled_login_form.cleaned_data["password"]
            try:
                    user_data=User.objects.get(email=login_email)
                    user=authenticate(request,username=user_data.username,password=login_password)
                    # if ret_email_or_mobile_from_db.password==login_password:

                    if user !=None:
                        login(request,user)
                    #     # request.session["member_id"]=ret_email_or_mobile_from_db.id
                    #     ## you are logged in
                    #     messages.success(request,"Login Success")
                        re_form=Login_form()

                        return redirect('home')

                    else:
                        re_form=Login_form()

                        # return render(request,"webapp1/Login1.html",{"Login_form":re_form,"status":"credentials are not matched"})
            except Exception as e:
                login_form=Login_form()
                messages.info(request,"credentials are mismatch!")
                return render(request,'webapp1/Login1.html',{"Login_form":login_form})

    # login_form=AuthenticationForm()
    login_form=Login_form()
    return  render(request,'webapp1/Login1.html',{"Login_form":login_form})



def logoutview(request):
    logout(request)
    # redirect('Login')
    return render(request,'webapp1/logout.html')
    # try:
    #     del request.session["member-id"]
    # except KeyError:
    #     pass
    # return HttpResponse("You're logged out.")



def Project_form_view(request):
    try:
        if request.method=="POST":
            filled_project_idea=Project_form(request.POST)
            if filled_project_idea.is_valid():
                title=filled_project_idea.cleaned_data["pro_form_title"]
                email=filled_project_idea.cleaned_data["Project_Email"]
                desc=filled_project_idea.cleaned_data["Project_Description"]
                p_obj=Project_Ideas(pro_title=title,pro_email=email,pro_description=desc)

                # p_obj.save()
                from_email1 = settings.EMAIL_HOST_USER
                subject="Project Idea Submitted"
                current_site = get_current_site(request)
                message=render_to_string('webapp1/project_email.html',
                                         {'user':request.user.username,
                                          "domain":current_site.domain,
                                          'food':"food",
                                          'login':'login',
                                          }
                                         )
                sender=settings.EMAIL_HOST_USER
                receiver=request.user.email
                # sending messages to mail
                reg_email = request.user.email
                if reg_email==email:
                    try:
                    # reg_email=request.user.email
                    # if reg_email==email:
                        send_mail(subject, message, sender, [email])
                        p_obj.pro_status="project Submitted"
                        p_obj.save()
                        messages.info(request, 'Project Idea Submitted will get back to you soon')
                        return render(request, 'webapp1/idea_status.html')
                    # else:
                    #     messages.error(request,"your registed mail id is ",reg_email ,"don't use other emails like",email)
                    #     return render(request,"webapp1/idea.html")

                    except:
                        pro_form = Project_form()
                        return render(request, 'webapp1/idea.html',
                                  {"pro_form": pro_form, "status": "please check your internet connection"})

                else:
                    status="your registed mail id is '{}' don't use other emails like '{}' ".format(reg_email,email)
                    pro_form=Project_form()
                    return render(request,"webapp1/idea.html",{"pro_form": pro_form,"status_pro":status})
        pro_form=Project_form()
        return render(request,'webapp1/idea.html',{"pro_form":pro_form})
    except:
        pro_form = Project_form()
        return render(request, 'webapp1/idea.html', {"pro_form": pro_form,"status":"please check your internet connection"})

# class Pro_Indexview(generic.ListView):
#     model=Project_Ideas
#     template_name = "webapp1/submitted_ideas.html"
#     def Ret(self):
#         return  Project_Ideas.objects.all()
#{% for i in object_list %}


def Pro_Indexview(request):
    model=Project_Ideas
    # return render(request,"webapp1/submitted_ideas.html",{"user":request.user})
    all_projects=Project_Ideas.objects.filter(pro_email=request.user.email)
    return  render(request,"webapp1/submitted_ideas.html",{"all_projects":all_projects,"owner":request.user.email})

def Project_statusView(request,pk):
    obj=Project_Ideas.objects.get(pk=pk)
    messages.info(request,"project status")
    return render(request, "webapp1/submitted_ideas.html",{"status":obj.pro_status})


def UpdateView(request):

    if request.method=="POST":
        try:
            filled_edit_form=update_profile(request.POST)
            if filled_edit_form.is_valid():
                form_email=filled_edit_form.cleaned_data["Email"]
                form_username=filled_edit_form.cleaned_data["username"]

                ret_data_from_model=User.objects.get(email=request.user.email)
                ret_data_from_model.username=form_username
                ret_data_from_model.email=form_email
                ret_data_from_model.save()


                request.user.email=form_email
                ## if form data updated then display form data
                # cu_user = request.user
                data = User.objects.get(email=request.user.email)
                data = {"username": data.username, "Email": data.email}
                # return  render(request,'webapp1/a.html',{"user":data})
                # request.user.username ,email ,password,mobile etc

                form = update_profile(data)

                if form:
                    messages.success(request,"Profile updated successfully")
                    return  render(request,'webapp1/update_profile.html',{"update_profile_data":form})
                else:
                    messages.error(request,"Profile not updated")
                    return render(request, 'webapp1/update_profile.html', {"update_profile_data": form})
        except :
            data = User.objects.get(email=request.user.email)
            data = {"username": data.username, "Email": data.email}
            form=update_profile(data)
            messages.info(request,"your update details alreday someone had")
            return render(request, 'webapp1/update_profile.html', {"update_profile_data": form})
    cu_user=request.user.email
    data=User.objects.get(email=cu_user)
    data = {"username": data.username, "Email": data.email}
    # return  render(request,'webapp1/a.html',{"user":data})
    # request.user.username ,email ,password,mobile etc

    form=update_profile(data)
    # return render(request,'webapp1/s2.html',{"all_data":request.user.email})
    return render(request,"webapp1/update_profile.html",{"update_profile_data":form,"all_data":request.user})






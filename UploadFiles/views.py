from django.shortcuts import redirect, render
from .forms import MyFileForm
from .models import MyFileUpload
from django.contrib import messages
import os
from UploadFiles.forms import NewUserForm
from UploadFiles.forms import login_form
# from UploadFiles.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import JsonResponse
from django.contrib.auth.decorators import *



# from django.contrib.auth.decorators import login_required

# Create your views here.

def user_perm(user):
    return user.is_staff
# @user_passes_test(user_perm,login_url='')

@user_passes_test(user_perm,login_url='login')
def home(request):
    if request.session.get('has_commented', False):
        mydata = MyFileUpload.objects.all()
        # print(User.objects.filter(username=request.user.username).values('username'))
        print(User.objects.values('username').exclude(username = 'admin'))
        usernames = User.objects.values('username').exclude(username = 'admin')
        myform = MyFileForm()
        if mydata != '':
            context = {'form': myform, 'mydata': mydata,'usernames': usernames}
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')
    # else:
    #     print("wrong")
    #     form = AuthenticationForm()
    #     return render(request=request, template_name="login/login.html", context={"login_form": form})
    #     # return render(request,"index.html",context)


def uploadfile(request):
    if request.method == "POST":
        myform = MyFileForm(request.POST, request.FILES)
        if myform.is_valid():
            Upload_Preson_Name = request.POST.get('uploader_name')
            MyFile = request.FILES.get('file')
            exists = MyFileUpload.objects.filter(my_file=MyFile).exists()            
            Date = request.POST['date']
            Flour = request.POST.getlist('dropdown')

            # if exists:
            #     messages.error(request,'The file %s is already exists...!!!'% MyFile)
            # else:
            MyFileUpload.objects.create(
                uploader_name=Upload_Preson_Name, my_file=MyFile, date=Date, flour=Flour).save()
            messages.success(request, "File uploaded successfully.")
        return redirect("home")


def deleteFile(request, id):
    mydata = MyFileUpload.objects.get(id=id)
    mydata.delete()
    os.remove(mydata.my_file.path)
    messages.success(request, 'File deleted successfully.')
    return redirect('home')


def homepage(request):
    return render(request=request, template_name="index.html")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, "Registration successful." )
            return redirect("home")
        # messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="login/registration.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['has_commented'] = True
                print(request.user.is_staff)
                if request.user.is_staff:
                # messages.info(request, f"You are now logged in as {username}.")
                    return redirect("home")
                else:     
                    return redirect("show")          
            else:
                print("Invalid username or password.")
        else:
            print("Invalid username or password.")
    if request.method == "GET":
        if request.session.get('has_commented', False):
            if request.user.is_staff:
                return redirect("home")
            else:     
                return redirect("show")
        else:        
            form = AuthenticationForm()    
            return render(request=request, template_name="login/login.html", context={"login_form": form})


def logout_request(request):
    print("logout")
    logout(request)
    request.session.clear()
    # messages.info(request, "You have successfully logged out.")
    return redirect("login")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "login/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="login/password/password_reset.html", context={"password_reset_form": password_reset_form})

def jsondata(request):
    data = list(MyFileUpload.objects.values())
    return JsonResponse(data, safe=False)

def show(request):
    return render(request=request, template_name="login/show1.html")

def jsonuserdata(request):
    data = list(User.objects.filter(username=request.user.username).values('username'))
    return JsonResponse(data, safe=False)

def a(request):
    return render(request=request, template_name="a.html")
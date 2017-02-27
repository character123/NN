#coding = utf-8
from django.shortcuts import render_to_response,render
from .models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label="username",max_length=20,required=True,error_messages={'required':"Please input the username"})
    password = forms.CharField(label="password",max_length=50,required=True,error_messages={'required':"Please input the password"})

class  AdministratorForm(forms.Form):
    username = forms.CharField(label="adminname",max_length=20)
    password = forms.CharField(label="adminpassword",max_length=50)

@csrf_exempt
def home(request):
    username = request.POST.get('username', None)
    if username:
        request.session['username'] = username
    username = request.session.get('username', None)
    if username:
        return render_to_response('home.html', )
    else:
        return render_to_response('login.html')

@csrf_exempt
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            User.objects.create(username = username,password = password)
            return render_to_response("input.html")#register successful
    else:
        uf = UserForm()
    return render_to_response('login.html')

@csrf_exempt
def login(request):
    # if user has logined
    if request.COOKIES.has_key("username"):
        return render_to_response("home.html")
    # if user has not logined
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                # login successfully
                response = render_to_response('home.html')
                response.set_cookie('username',username,3600)
                return response
            else:
                # login unsuccessfully
                return render_to_response("login.html")
        else:
            return render_to_response("home.html")
    else:
        uf = UserForm()
    return render_to_response('login.html')


def index(request):#login successful
    username = request.COOKIES.get('username','')
    return render_to_response('index.html',{'username':username})

def logout(request):
    username = request.COOKIES.get('username','')
    response = HttpResponse('logout!')
    response.delete_cookie('username')
    return response


@csrf_exempt
def input(request):
    return render_to_response('input.html')

@csrf_exempt
def output(request):
    if request.method == "POST":
        myFile = request.FILES.get("JPEG",None)
        if not myFile:
            return render_to_response("/output.html/")
        destination = open(os.path.join("C:\Users\Yzc\NN\Web\upload",myFile.name),'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        return render_to_response("output.html")
    else:
        return render_to_response('output.html')


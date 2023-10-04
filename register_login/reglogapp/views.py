from django.shortcuts import render,redirect
from reglogapp.forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def index(request):
    data = User.objects.all()
    context = {'data':data}

    return render(request,'index.html', context)


def reg(request):
   
    if request.method=='POST':
        form = NewUserForm(request.POST)
       
        if form.is_valid():
            form.save()
            messages.success(request,"registration successful...")
            return redirect('/login')
        else:
            messages.error(request,"Unsuccessful registration. Invalid information.")
            return redirect('/')

    else:    
        form = NewUserForm()
        context = {'form':form}
        return render(request,'register.html',context)


def log(request):
    if request.method=='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None and user.is_staff==True:
                login(request,user)
                messages.info(request,f"You are logged in {username}")
                return redirect('/index')
            else:
               messages.warning(request,"Invalid username or password..") 
        else:
            messages.warning(request,"Invalid username or password..")
    form = AuthenticationForm()
    context = {'form':form}
    return render(request,'login.html',context)
def userlogin(request):
    if request.method=='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None and user.is_staff==False:
                login(request,user)
                messages.info(request,f"You are logged in {username}")
                return redirect('/index')
            else:
               messages.warning(request,"Invalid username or password..") 
        else:
            messages.warning(request,"Invalid username or password..")
    form = AuthenticationForm()
    context = {'form':form}
    return render(request,'userlogin.html',context)

@login_required
def logout_req(request):
    logout(request)
    messages.info(request,"You are Logged out..")
    return redirect('/login')



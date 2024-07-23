from django.shortcuts import render,redirect
from . models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'base.html')

def categories(request):
    item=Category.objects.all()
    return render(request,'category.html',{'item':item})

def buy(request,i):
    cat=Category.objects.get(id=i)
    pro1=Product.objects.filter(category=i)
    return render(request,'buy.html',{'cat':cat,'pro1':pro1})


def product(request,i):
    # cat1=Category.objects.get(id=i)
    product=Product.objects.get(id=i)
    return render(request,'product.html',{'product':product})

def register(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        cp=request.POST['cp']
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']

        if cp==p:
            u = User.objects.create_user(username=u, password=p, first_name=fn, last_name=ln, email=e)
            u.save()
            return redirect('shop:home')
        else:
            messages.error(request, 'Passwords are not same')

    return render(request,'register.html')

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']

        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, "Invalid Entry")

    return render(request,'login.html')
@login_required()
def user_logout(request):
    logout(request)
    return redirect('/login')
from django.shortcuts import render
from . models import *
from shop.forms import CustomUserForm
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json


# Create your views here.

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'shop/home.html',{'products':products})

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success You can Login Now..!')
            return HttpResponseRedirect(reverse('user_login'))
    return render(request,'shop/register.html',{'form':form})

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully')
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request,'Invalid Username or Password')
                return HttpResponseRedirect(reverse('user_login'))
        return render(request,'shop/user_login.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged out successfully')
        return HttpResponseRedirect(reverse('home'))

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'shop/collections.html',{'catagory':catagory})

def collectionsview(request,name):
    if (Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,'shop/products/index.html',{'products':products,'catagory_name':name})
    else:
        messages.warning(request,'No such catagory found')
        return HttpResponseRedirect(reverse('collections'))
    
def product_details(request,cname,pname):
    if (Catagory.objects.filter(name=cname,status=0)):
        if (Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{'products':products})
        else:
            messages.error(request,'No such product found')
            return HttpResponseRedirect(reverse('collections'))

    else:
        messages.error(request,'No such catagory found')
        return HttpResponseRedirect(reverse('collections'))
    
def cart(request):
    if request.headers.get('X-requested-width')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product already is cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not available'},status=200)

        else:
            return JsonResponse({'status':'Login to Add cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'cart':cart})
    else:
        return HttpResponseRedirect(reverse('home'))
    
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return HttpResponseRedirect(reverse('cart_page'))

def fav(request):
    if request.headers.get('X-requested-width')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favorite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product already is Favorite'},status=200)
                else:
                    Favorite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product added to Favorite'},status=200)
           
        else:
            return JsonResponse({'status':'Login to Add Favorite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def fav_page(request):
    if request.user.is_authenticated:
        fav=Favorite.objects.filter(user=request.user)
        return render(request,'shop/fav.html',{'fav':fav})
    else:
        return HttpResponseRedirect(reverse('home'))
    

def remove_fav(request,fid):
    favitem=Favorite.objects.get(id=fid)
    favitem.delete()
    return HttpResponseRedirect(reverse('fav_page'))

from django.shortcuts import render
from django.http import HttpResponse
from .models import Products
from math import ceil
from django.db.models import Count

def index(request):
    allprods = []
    catprods=Products.objects.values('category','id')
    cats= {item['category'] for item in catprods}
    for cat in cats:
        prod=Products.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        allprods.append([prod,range(1, nSlides),nSlides])
    param={'allprods':allprods}
    print(param)
    return render(request,'shop/index.html',param)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    return render(request,'shop/contact.html')

def tracker(request):
    return render(request,'shop/tracker.html')

def search(request):
    return HttpResponse("we are at search")

def productView(request):
    return HttpResponse("we are at prodview")

def checkout(request):
    return HttpResponse("we are at checkout")

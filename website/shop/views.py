from django.shortcuts import render
from django.http import HttpResponse
from .models import Products,Contact,Order,OrderUpdate
from math import ceil
from django.db.models import Count
import json

def index(request):
    return render(request,'shop/login.html')

def main(request):
    allprods = []
    catprods=Products.objects.values('category','id')
    cats= {item['category'] for item in catprods}
    for cat in cats:
        prod=Products.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        allprods.append([prod,range(1, nSlides),nSlides])
    param={'allprods':allprods}
    return render(request,'shop/main.html',param)

def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    allprods = []
    catprods=Products.objects.values('category','id')
    cats= {item['category'] for item in catprods}
    for cat in cats:
        prodtemp=Products.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        if len(prod)!=0:
            allprods.append([prod,range(1, nSlides),nSlides])
    param={'allprods':allprods,'msg':""}
    if len(allprods)==0:
        param={'msg':"Please make sure to enter relevant search query"}
    return render(request,'shop/main.html',param)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True
        return render(request,'shop/contact.html',{'thank':thank})
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')
        try:
            order=Order.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse("{}")
    return render(request,'shop/tracker.html')

def productView(request,myid):
    product=Products.objects.filter(id=myid)
    return render(request,'shop/productView.html',{'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json=request.POST.get('itemJson','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        order=Order(items_json=items_json,name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')

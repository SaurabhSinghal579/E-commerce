from django.contrib import admin

from .models import Products,Contact,Order,OrderUpdate
admin.site.register(Products)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)

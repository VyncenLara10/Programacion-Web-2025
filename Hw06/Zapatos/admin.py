from django.contrib import admin
from .models import Customer, Shoe, Order, OrderItem

admin.site.register(Customer)
admin.site.register(Shoe)
admin.site.register(Order)
admin.site.register(OrderItem)
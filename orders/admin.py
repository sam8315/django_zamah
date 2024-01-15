from django.contrib import admin
from .models import *


# admin.site.register(Order)
# admin.site.register(OrderItem)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('order', 'product', 'quantity', 'price',)
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('user', 'is_paid', 'first_name', 'last_name', 'phone_number', 'created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('order', 'product', 'quantity', 'price',)

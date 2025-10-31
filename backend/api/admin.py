from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','stock')
    search_fields = ('name','description')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','quantity','added_at')
    search_fields = ('user__email','product__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total','status','created_at')
    inlines = [OrderItemInline]


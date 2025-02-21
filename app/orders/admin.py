from django.contrib import admin
from .models import Order, Order_Item

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'total_price', 'status', 'created_at', 'payment_method', 'payment_status')
    search_fields = ('user_id__username', 'status', 'payment_status')
    list_filter = ('status', 'payment_status')
    ordering = ('-created_at',)

@admin.register(Order_Item)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'pc_id', 'component_id', 'order_type', 'quantity')
    search_fields = ('order_id__id', 'order_type')
    list_filter = ('order_type',)
    ordering = ('order_id',)


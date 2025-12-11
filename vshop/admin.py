from django.contrib import admin
from .models import Product, Order, Transaction
from .models import Cart, CartItem
from .models import Category


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')  # columns to show
    list_filter = ('status', 'created_at')  # filters on the right
    search_fields = ('user__username', 'id')  # search by user or order ID

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'order', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'user_username', 'order_id')

# Register your models here.

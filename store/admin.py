from django.contrib import admin
from .models import Category, Product, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# --- ADMIN DE PEDIDOS ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'total')
    list_filter = ('user', 'created')
    readonly_fields = ('user', 'created', 'total')


# --- ADMIN DE USUARIOS (SIN INLINES) ---
class UserAdmin(BaseUserAdmin):
    pass


# --- REGISTRO EN EL ADMIN ---
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(Product)

from django.contrib import admin
from .models import ShoppingList, Item

# Register your models here.

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'user__username')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'shopping_list', 'quantity', 'unit', 'price', 'purchased')
    list_filter = ('purchased', 'shopping_list')
    search_fields = ('name', 'shopping_list__title')

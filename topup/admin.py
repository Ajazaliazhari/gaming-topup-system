from django.contrib import admin
from .models import Game, TopUpProduct, TopUpOrder

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_id', 'is_active')
    search_fields = ('name', 'game_id')

@admin.register(TopUpProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'game')
    search_fields = ('name',)
    list_filter = ('game',)


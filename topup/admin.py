from django.contrib import admin

from .models import Game, TopUpProduct, TopUpOrder

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Game model.
    """
    list_display = ('name', 'game_id', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'game_id')
    prepopulated_fields = {'game_id': ('name',)} # Optional: auto-populate game_id from name for convenience

@admin.register(TopUpProduct)
class TopUpProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TopUpProduct model.
    """
    list_display = ('name', 'game', 'price', 'in_game_currency')
    list_filter = ('game', 'price')
    search_fields = ('name', 'game__name', 'in_game_currency')
    raw_id_fields = ('game',) # Use raw ID for ForeignKey for better performance with many games
    list_select_related = ('game',) # Optimize foreign key lookups

@admin.register(TopUpOrder)
class TopUpOrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TopUpOrder model.
    """
    list_display = ('id', 'user_email', 'product', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'product__game')
    search_fields = ('user_email', 'product__name', 'id')
    raw_id_fields = ('product',) # Use raw ID for ForeignKey
    readonly_fields = ('created_at',)
    list_select_related = ('product', 'product__game') # Optimize foreign key lookups

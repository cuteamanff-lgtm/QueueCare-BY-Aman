from django.contrib import admin
from .models import Token

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("token_number", "full_name", "service", "status", "priority", "created_at")
    list_filter = ("status", "service", "priority", "created_at")
    search_fields = ("token_number", "full_name", "mobile_number")

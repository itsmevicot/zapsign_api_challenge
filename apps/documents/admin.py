from django.contrib import admin
from apps.documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Document model.
    """
    list_display = ('id', 'name', 'status', 'company', 'created_by', 'created_at', 'last_updated_at')
    list_filter = ('status', 'company', 'created_at', 'last_updated_at')
    search_fields = ('name', 'created_by', 'token', 'external_id')
    readonly_fields = ('created_at', 'last_updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'status', 'company', 'created_by')
        }),
        ('Document Details', {
            'fields': ('open_id', 'token', 'external_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated_at')
        }),
    )

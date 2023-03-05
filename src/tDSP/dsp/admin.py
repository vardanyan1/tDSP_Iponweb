from django.contrib import admin
from django.utils.html import format_html

from .models.admin_model import AdminModel
from .models.ad_ops_model import AdOpsModel


class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'photo_name')

    @admin.display(description='Photo')
    def photo_name(self, obj):
        if obj.photo:
            return format_html('<a href="{}">...{}</a>', obj.photo.url, obj.photo.name[-12:])


class AdOpsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'photo_name')

    @admin.display(description='Photo')
    def photo_name(self, obj):
        if obj.photo:
            return format_html('<a href="{}">...{}</a>', obj.photo.url, obj.photo.name[-12:])


admin.site.register(AdminModel, AdminAdmin)
admin.site.register(AdOpsModel, AdOpsAdmin)

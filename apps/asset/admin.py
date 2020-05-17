from django.contrib import admin

from apps.asset.models import Asset


class AssetAdmin(admin.ModelAdmin):
    model = Asset
    list_display = ["name", "category", "creation_date"]


admin.site.register(Asset, AssetAdmin)

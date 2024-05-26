from django.contrib import admin

from customs.models import Custom,CustomItem

# admin.site.register(Custom)
# admin.site.register(CustomItem)

class CustomItemTabulareAdmin(admin.TabularInline):
    model = CustomItem
    fields = "product", "name", "price", "quantity"
    search_fields = (
        "product",
        "name",
    )
    extra = 0


@admin.register(CustomItem)
class CustomItemAdmin(admin.ModelAdmin):
    list_display = "custom", "product", "name", "price", "quantity"
    search_fields = (
        "custom",
        "product",
        "name",
    )


class CustomTabulareAdmin(admin.TabularInline):
    model = Custom
    fields = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
    )
    inlines = (CustomItemTabulareAdmin,)

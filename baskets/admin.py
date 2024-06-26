from django.contrib import admin

from baskets.models import Basket


# admin.site.register(Basket)

class BasketTabAdmin(admin.TabularInline):
    model = Basket
    fields = "product", "quantity", "created_timestamp"
    search_fields = "product", "quantity", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user_display','product_display','quantity','created_timestamp',]
    list_filter = ['created_timestamp','user','product__name',]

    def user_display(self,obj):
        if obj.user:
            return str(obj.user)
        return "Не зареєстрований користувач"

    def product_display(self,obj):
        return str(obj.product.name)



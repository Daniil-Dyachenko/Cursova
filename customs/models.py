from django.db import models
from sushi.models import Products

from users.models import User


class CustomitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Custom(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Користувач",
                             default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення замовлення")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону")
    requires_delivery = models.BooleanField(default=False, verbose_name="Доставка")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адреса доставки")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при отриманні ")
    is_paid = models.BooleanField(default=False, verbose_name="Сплачено")
    status = models.CharField(max_length=50, default='Опрацювується', verbose_name="Статус замовлення")

    class Meta:
        db_table = "custom"
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлень"

    def __str__(self):
        return f"Замовлення № {self.pk} | Одержувач {self.user.first_name} {self.user.last_name}"


class CustomItem(models.Model):
    custom = models.ForeignKey(to=Custom, on_delete=models.CASCADE, verbose_name="Замовлення")
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт",
                                default=None)
    name = models.CharField(max_length=150, verbose_name="Назва")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажу")

    class Meta:
        db_table = "custom_item"
        verbose_name = "Продане замовлення"
        verbose_name_plural = "Продані замовлення"

    objects = CustomitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Продукт {self.name} | Замовлення № {self.custom.pk}"
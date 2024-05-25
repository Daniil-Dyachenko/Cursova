from django.db import models

from sushi.models import Products
from users.models import User


class BasketQuerySet(models.QuerySet):

    def total_price(self):
        return sum(basket.products_price() for basket in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE,blank=True, null=True, verbose_name='Користувач')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE,verbose_name='Продукт')
    quantity = models.PositiveSmallIntegerField(default=0,verbose_name='Сумарна кількість')
    session_key = models.CharField(max_length=32,blank=True,null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')

    class Meta:
        db_table = 'basket'
        verbose_name = "Кошик"
        verbose_name_plural = "Кошик"

    objects = BasketQuerySet().as_manager()
    def products_price(self):
        return round(self.product.sell_price() * self.quantity , 2)

    def __str__(self):
        return f'Кошик{self.user.username} | Продукт {self.product.name} | Кількість {self.quantity}'

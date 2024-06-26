from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images',blank=True,null=True, verbose_name='Фотографія')
    phone_number = models.CharField(max_length=11,blank=True,null=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'Користувача'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.username
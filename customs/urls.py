from django.urls import path

from customs import views

app_name = 'customs'

urlpatterns = [
    path('create-custom/',views.create_customs, name = 'create_customs'),
]
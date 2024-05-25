from django.shortcuts import render
from django.shortcuts import redirect

from sushi.models import Products
from baskets.models import Basket

def basket_add(request,product_slug):

    product = Products.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user,product=product)

        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity +=1
                basket.save()
        else:
            Basket.objects.create(user=request.user,product=product,quantity=1)

    return redirect(request.META['HTTP_REFERER'])



def basket_change(request,product_slug):
    ...

def basket_remove(request,basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])
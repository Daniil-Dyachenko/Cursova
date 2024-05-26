from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

from sushi.models import Products
from baskets.models import Basket
from baskets.utils import get_user_baskets

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

    else:
        baskets = Basket.objects.filter(session_key=request.session.session_key, product=product)

        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            Basket.objects.create(session_key=request.session.session_key, product=product,quantity=1)

    return redirect(request.META['HTTP_REFERER'])


def basket_change(request):
    basket_id = request.POST.get('basket_id')
    basket = get_object_or_404(Basket, id=basket_id)

    if 'increment' in request.POST:
        basket.quantity += 1
    elif 'decrement' in request.POST and basket.quantity > 1:
        basket.quantity -= 1

    basket.save()

    messages.add_message(request, messages.SUCCESS, 'Кількість товару успішно оновлено.')

    return redirect('user:users_basket')

def basket_remove(request,basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])


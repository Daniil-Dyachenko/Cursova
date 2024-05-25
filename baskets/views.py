from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string

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


def basket_change(request,product_slug):
    basket_id = request.POST.get("basket_id")
    quantity = request.POST.get("quantity")

    basket = Basket.objects.get(id=basket_id)

    basket.quantity = quantity
    basket.save()
    update_quantity = basket.quantity

    basket = get_user_baskets(request)
    basket_items_html = render_to_string('baskets/includes/included_basket.html', {"baskets":basket}, request=request)

    response_data = {
        "message": "Кількість змінена",
        "basket_items_html": basket_items_html,
        "quantity": update_quantity
    }

    return JsonResponse(response_data)

def basket_remove(request,basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])


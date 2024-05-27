from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect

from baskets.models import Basket

from customs.forms import CreateCustomForm
from customs.models import Custom, CustomItem

@login_required
def create_customs(request):
    if request.method == 'POST':
        form = CreateCustomForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    basket_items = Basket.objects.filter(user=user)

                    if basket_items.exists():
                        custom = Custom.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        for basket_item in basket_items:
                            product = basket_item.product
                            name = basket_item.product.name
                            price = basket_item.product.sell_price()
                            quantity = basket_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Таких продуктів на данний момент немає {name} \
                                                           В наявності - {product.quantity}')

                            CustomItem.objects.create(
                                custom=custom,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        basket_items.delete()

                        messages.success(request, 'Замовлення прийнято!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('basket:custom')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = CreateCustomForm(initial=initial)

    context = {
        'title': 'Акамедзутсу - Оформлення замовлення',
        'form': form,
        'custom': True,
    }
    return render(request, 'customs/create_custom.html', context=context)

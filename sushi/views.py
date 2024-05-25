from django.shortcuts import render
from django.shortcuts import get_list_or_404
from django.core.paginator import Paginator
from sushi.models import Products
from sushi.utils import q_search

def catalog(request,category_slug=None):

    page = request.GET.get('page',1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q',None)


    if category_slug == "all":
        sushi = Products.objects.all()

    elif query:
        sushi = q_search(query)

    else:
        sushi = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        sushi = sushi.filter(discount__gt=0)

    if order_by and order_by != "default":
        sushi = sushi.order_by(order_by)

    paginator = Paginator(sushi,3)
    page = paginator.page(int(page))

    context = {
        'title': 'Sushi-Bar - Каталог',
        'goods': page,
        'slug_url': category_slug,
    }
    return render(request, 'sushi/catalog.html', context)

def product(request,product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {
        "product": product
    }

    return render(request, 'sushi/product.html',context=context)

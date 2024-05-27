from django.shortcuts import render
from django.contrib import auth,messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from users.forms import UserLoginForm
from users.forms import UserRegistrationForm
from users.forms import ProfileForm
from baskets.models import Basket
from customs.models import Custom, CustomItem

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                messages.success(request,f"{username}, Ви успішно ввійшли до свого аккаунту")
                direct_page = request.POST.get('next', None)
                if direct_page and direct_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Акамедзутсу - Авторизація',
        'form': form
    }
    return render(request,'users/login.html',context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request,user)
            messages.success(request, f"{user.username}, Ви успішно зареєструвались і увійшли до свого аккаунту")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Акамедзутсу - Регістрація',
        'form': form
    }
    return render(request,'users/registration.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST,instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ви успішно оновили свій профіль")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

        customs = Custom.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                "customitem_set",
                queryset=CustomItem.objects.select_related("product"),
            )
        ).order_by("-id")

    context = {
        'title': 'Акамедзутсу - Особистий кабінет',
        'form': form,
        'customs' : customs
    }
    return render(request,'users/profile.html',context)

def users_basket(request):
    return render(request,'users/users_basket.html')



@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Ви успішно вийшли із свого аккаунту")
    auth.logout(request)
    return redirect(reverse('main:index'))

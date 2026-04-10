from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Account

# Dish Crud

def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes': dish_objects})


def add_menu(request):
    if request.method == "POST":
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')

        Dish.objects.create(
            name=dishname,
            cook_time=cooktime,
            prep_time=preptime
        )
        return redirect('better_menu')

    return render(request, 'tapasapp/add_menu.html')


def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})


def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')


def update_dish(request, pk):
    d = get_object_or_404(Dish, pk=pk)

    if request.method == "POST":
        d.cook_time = request.POST.get('ctime')
        d.prep_time = request.POST.get('ptime')
        d.save()
        return redirect('view_detail', pk=pk)

    return render(request, 'tapasapp/update_menu.html', {'d': d})

# AUTH SYSTEM


def login_view(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = Account.objects.filter(username=username, password=password).first()

        if user:
            return redirect('better_menu')
        else:
            message = "Invalid login"

    return render(request, 'login.html', {'message': message})


def signup_view(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Account.objects.filter(username=username).exists():
            message = "Account already exists"
        else:
            Account.objects.create(username=username, password=password)
            return redirect('login')

    return render(request, 'signup.html', {'message': message})

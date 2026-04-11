from django.shortcuts import get_object_or_404, redirect, render

from .models import Account, Dish


# DISH CRUD SYSTEM

def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes': dish_objects})


def add_menu(request):
    if request.method == "POST":
        Dish.objects.create(
            name=request.POST.get('dname'),
            cook_time=request.POST.get('ctime'),
            prep_time=request.POST.get('ptime')
        )
        return redirect('better_menu')

    return render(request, 'tapasapp/add_menu.html')


def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})


def update_dish(request, pk):
    d = get_object_or_404(Dish, pk=pk)

    if request.method == "POST":
        d.cook_time = request.POST.get('ctime')
        d.prep_time = request.POST.get('ptime')
        d.save()
        return redirect('view_detail', pk=pk)

    return render(request, 'tapasapp/update_menu.html', {'d': d})


def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')


# AUTH SYSTEM

def login_view(request):
    message = ""
    success_message = request.GET.get('message', "")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Account.objects.filter(username=username, password=password).first()

        if user:
            return redirect('basic_list', pk=user.id)

        message = "Invalid login"

    return render(request, 'tapasapp/login.html', {
        'message': message,
        'success_message': success_message,
    })


def signup_view(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Account.objects.filter(username=username).exists():
            message = "Account already exists"
        else:
            Account.objects.create(username=username, password=password)
            return redirect('/?message=Account created successfully')

    return render(request, 'tapasapp/signup.html', {'message': message})


def basic_list(request, pk):
    user = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/basic_list.html', {'user': user})


def manage_account(request, pk):
    user = get_object_or_404(Account, id=pk)
    return render(request, 'tapasapp/manage_account.html', {'user': user})


def change_password(request, pk):
    user = get_object_or_404(Account, id=pk)
    message = ""

    if request.method == "POST":
        if 'cancel' in request.POST:
            return redirect('manage_account', pk=pk)

        current = request.POST.get('current')
        new = request.POST.get('new')
        confirm = request.POST.get('confirm')

        if current == user.password and new == confirm:
            user.password = new
            user.save()
            return redirect('manage_account', pk=pk)

        message = "Invalid input"

    return render(request, 'tapasapp/change_password.html', {
        'user': user,
        'message': message,
    })


def delete_account(request, pk):
    get_object_or_404(Account, id=pk).delete()
    return redirect('login')


def logout_view(request):
    return redirect('login')

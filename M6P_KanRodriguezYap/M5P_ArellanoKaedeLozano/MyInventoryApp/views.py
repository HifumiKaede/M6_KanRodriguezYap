from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, WaterBottle, Account

def view_supplier(request):
    if not request.session.get("account_id"):
        return redirect("login")
    suppliers = Supplier.objects.all()
    account_id = request.session.get("account_id")
    return render(request, "view_supplier.html", {"suppliers": suppliers, "account_id": account_id})

def logout_view(request):
    request.session.flush()
    return redirect("login")

def view_bottles(request):
    if not request.session.get("account_id"):
        return redirect("login")
    bottles = WaterBottle.objects.all()
    return render(request, "view_bottles.html", {"water_bottles": bottles})

def add_bottle(request):
    if not request.session.get("account_id"):
        return redirect("login")

    suppliers = Supplier.objects.all()

    if request.method == "POST":
        supplier = get_object_or_404(Supplier, pk=request.POST.get("supplied_by"))

        WaterBottle.objects.create(
            SKU=request.POST.get("sku"),
            brand=request.POST.get("brand"),
            cost=request.POST.get("cost"),
            size=request.POST.get("size"),
            mouth_size=request.POST.get("mouth_size"),
            color=request.POST.get("color"),
            supplied_by=supplier,
            current_quantity=request.POST.get("current_quantity")
        )

        return redirect("view_bottles")

    return render(request, 'add_bottle.html', {'suppliers': suppliers})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            account = Account.objects.get(username=username, password=password)
            request.session["account_id"] = account.id
            return redirect("view_supplier")
        except Account.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid login"})
    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if Account.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Account already exists"})
        Account.objects.create(username=username, password=password)
        return render(request, "login.html", {"success": "Account created successfully"})
    return render(request, "signup.html")

def manage_account(request, pk):
    if not request.session.get("account_id"):
        return redirect("login")
    account = get_object_or_404(Account, pk=pk)
    return render(request, "manage_account.html", {"account": account})

def view_bottle_details(request, pk):
    if not request.session.get("account_id"):
        return redirect("login")

    bottle = get_object_or_404(WaterBottle, pk=pk)
    return render(request, "view_bottle_details.html", {"bottle": bottle})

def delete_bottle(request, pk):
    if not request.session.get("account_id"):
        return redirect("login")

    bottle = get_object_or_404(WaterBottle, pk=pk)
    bottle.delete()
    return redirect("view_bottles")

def delete_account(request, pk):
    if not request.session.get("account_id"):
        return redirect("login")
    account = get_object_or_404(Account, pk=pk)
    account.delete()
    request.session.flush()
    return redirect("login")

def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    message = ""

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if current password is correct
        if current_password != account.getPassword():
            message = "Incorrect current password"

        # Check if new passwords match
        elif new_password != confirm_password:
            message = "Passwords do not match"

        else:
            account.password = new_password
            account.save()
            return redirect('manage_account', pk=account.pk)

    return render(request, 'change_password.html', {
        'account': account,
        'message': message
    })

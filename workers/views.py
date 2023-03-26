from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Worker
from products.models import Product, Purchase

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


@login_required
def home(request):
    worker, created = Worker.objects.get_or_create(user=request.user)
    first_name = worker.first_name
    last_name = worker.last_name
    email_ = worker.email
    money = worker.money
    data = {"first_name": first_name, "last_name": last_name, "email": email_, "money": money}
    return render(request, "landing/home.html", context=data)


@login_required
def user(request):
    worker = request.user.worker
    products = Product.objects.all()
    purchases = request.user.purchases.all()

    context = {
        'user': worker,
        'products': products,
        'purchases': purchases
    }
    return render(request, 'landing/user.html', context)


@login_required
def product_purchase(request, pk):
    product = get_object_or_404(Product, pk=pk)
    worker = request.user.worker
    if product.price <= worker.money:
        worker.money -= product.price
        purchase = Purchase(product=product, user=request.user)
        purchase.save()
        worker.save()
    return redirect('user')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'registration/login.html')

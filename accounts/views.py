from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from cart.models import Order, OrderItem


def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Your account has been created {username}. Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, 'register.html', context)


@login_required
def profile_view(request):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account info has been updated.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    orders = Order.objects.filter(
        customer=request.user, paid=True).order_by('-date_ordered')

    all_orders = []

    for order in orders:
        order_items_db = OrderItem.objects.filter(order=order)
        order_items = []
        order_total = 0
        for order_item in order_items_db:
            order_items.append(order_item)
            order_total += int(order_item.product.price * order_item.quantity)
        all_orders.append(
            {'order': order, 'order_items': order_items, "total": order_total})

    context = {
        'form': form,
        'all_orders': all_orders,
    }

    return render(request, 'profile.html', context)

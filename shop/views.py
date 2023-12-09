from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase
from .forms import PurchaseForm

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        product.quantity += 1
        product.save()
        return redirect('index')

    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'shop/purchase_form.html'
    success_url = 'cart/'

    def form_valid(self, form):
        form.instance.product_id = self.kwargs['product_id']
        return super().form_valid(form)


def cart(request):
    cart_items = Product.objects.filter(quantity__gt=0)
    total_items = sum(item.quantity for item in cart_items)
    context = {'cart_items': cart_items, 'total_items': total_items}
    return render(request, 'shop/cart.html', context)


def edit_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        if action == 'remove':
            product = Product.objects.get(pk=product_id)
            product.quantity = 0
            product.save()
        elif action == 'decrease':
            product = Product.objects.get(pk=product_id)
            product.decrease_quantity()

    cart_items = Product.objects.filter(quantity__gt=0)
    total_items = sum(item.quantity for item in cart_items)
    context = {'cart_items': cart_items, 'total_items': total_items}
    return render(request, 'shop/edit_cart.html', context)

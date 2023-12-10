from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase
from .forms import PurchaseForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView

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
    success_url = reverse_lazy('purchase_success')

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        form.instance.product_id = product_id
        form.save()

        product = Product.objects.get(pk=product_id)
        person = self.request.POST.get('person', '')
        address = self.request.POST.get('address', '')

        return render(self.request, 'shop/purchase_success.html',
                      {'product': product, 'person': person, 'address': address})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        product = Product.objects.get(pk=product_id)
        context['product_id'] = product_id
        context['product'] = product
        context['quantity'] = 1
        context['person'] = self.request.POST.get('person', '')
        context['address'] = self.request.POST.get('address', '')
        return context


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


class PurchaseSuccess(TemplateView):
    template_name = 'shop/purchase_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.request.GET.get('product_id')
        product = Product.objects.get(pk=product_id)
        person = self.request.GET.get('person', '')
        address = self.request.GET.get('address', '')

        context['product'] = product
        context['person'] = person
        context['address'] = address

        return context


class PurchaseCreateAll(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'shop/purchase_form.html'
    success_url = reverse_lazy('purchase_success_all')

    def form_valid(self, form):
        cart_items = Product.objects.filter(quantity__gt=0)

        for item in cart_items:
            Purchase.objects.create(product=item, person=form.cleaned_data['person'],
                                    address=form.cleaned_data['address'])

        context = {'cart_items': cart_items, 'person': form.cleaned_data['person'], 'address': form.cleaned_data['address']}
        return render(self.request, 'shop/purchase_success.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_id'] = None

        cart_items = Product.objects.filter(quantity__gt=0)
        context['quantity'] = sum(item.quantity for item in cart_items)

        context['cart_items'] = cart_items
        context['person'] = self.request.POST.get('person', '')
        context['address'] = self.request.POST.get('address', '')
        return context
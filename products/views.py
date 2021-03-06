import json
from decimal import Decimal
from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from .models import Product

# Create your views here.


class ListingDetailView(DetailView):
    """ Create view for individual listings """
    model = Product
    template_name = 'listing.html'
    context_object_name = 'product'
    extra_context = {}

    def get_object(self, queryset=Product):
        _id = self.kwargs.get('pk')
        instance = get_object_or_404(Product, id=_id)

        self.extra_context['product'] = instance
        self.extra_context['stock_arr'] = [
            x for x in range(instance.num_in_stock)]
        self.extra_context['more_products'] = Product.objects.all().filter(
            category=instance.category).exclude(id=_id).order_by('?')[:6]

        return instance

    def post(self, request, *args, **kwargs):

        form = json.loads(request.body)
        _id = self.kwargs.get('pk')
        instance = get_object_or_404(Product, id=_id)

        # checks if orderItems already exists in session storage,
        # and creates it if needed.
        cart = request.session.get(
            'cart', {'orderItems': [], 'total': 0, 'count': 0})

        item_already_in_cart = False
        too_many = False

        # if cart already exists, check if selected item
        # is already in cart orderItems
        if len(cart['orderItems']) != 0:
            for item in cart['orderItems']:
                listingId = item.get("listingId")

                # if listing is already in cart set to true,
                # check num in stock against num requested by user
                if listingId == _id:
                    item_already_in_cart = True
                    num_in_stock = instance.num_in_stock
                    quantity_total = int(
                        item['quantity']) + int(form['quantity'])

                    # if quantity requested is more than
                    # is in stock set quantity
                    # of item to number in stock and send
                    # response to js to alert user
                    if quantity_total > num_in_stock:
                        diff = quantity_total - num_in_stock
                        item['quantity'] = int(num_in_stock)
                        too_many = True
                    else:
                        item['quantity'] = int(quantity_total)

            # if item not already in cart, append new item to orderItems
            if not item_already_in_cart:
                cart['orderItems'].append(
                    {'listingId': _id, 'quantity': int(form['quantity'])})

        # if brand new cart, add first orderItem to it
        else:
            cart['orderItems'].append(
                {'listingId': _id, 'quantity': int(form['quantity'])})

        # set values for count and total for new item in cart
        if not too_many:
            cart['count'] = cart['count'] + int(form['quantity'])
            cart['total'] = round(
                cart['total'] + float(Decimal(instance.price)
                                      * Decimal(form['quantity'])))

        # set values for count and total based on the number of items
        # in stock rather than number of items user requested
        else:
            quantity_to_add = int(form['quantity']) - diff
            cart['count'] = cart['count'] + quantity_to_add
            cart['total'] = round(
                cart['total'] + float(Decimal(instance.price)
                                      * quantity_to_add))

        request.session['cart'] = cart

        data = {
            'title': instance.title,
            'quantity': form['quantity'],
            'too_many': too_many
        }
        return JsonResponse(data)


def categories_view(request, *args, **kwargs):
    """
    Display all categories for users to choose from.
    """
    return render(request, "categories.html")


class ProductMixin(ListView):

    model = Product
    template_name = 'results.html'
    queryset = Product.objects.all().order_by('-id')
    context_object_name = 'products'
    paginate_by = 12

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            sort = request.POST.get('results-sort-select')
            if sort == 'price-high':
                return redirect(reverse('all-products-price-high'))
            elif sort == 'price-low':
                return redirect(reverse('all-products-price-low'))
            elif sort == 'featured':
                return redirect(reverse('all-products'))


class AllProductsView(ProductMixin):
    """
    Inherits from custom built ProductMixin,
    collects context data need for this specific
    page to render all products page.
    with Products with featured=True first.
    """

    def get_queryset(self):
        featured = Product.objects.filter(featured=True)
        not_featured = Product.objects.filter(featured=False)
        queryset = list(chain(featured, not_featured))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllProductsView, self).get_context_data(**kwargs)
        context['category'] = 'All Products'
        context['select'] = 'featured'
        return context


class AllProductsPriceHighView(ProductMixin):
    """
    Inherits from custom built ProductMixin,
    collects context data need for this specific
    page to render all products page
    with highest priced listings first.
    """
    ordering = ['-price']

    def get_context_data(self, **kwargs):
        context = super(AllProductsPriceHighView,
                        self).get_context_data(**kwargs)
        context['category'] = 'All Products'
        context['select'] = 'price-high'
        return context


class AllProductsPriceLowView(ProductMixin):

    ordering = ['price']

    def get_context_data(self, **kwargs):
        context = super(AllProductsPriceLowView,
                        self).get_context_data(**kwargs)
        context['category'] = 'All Products'
        context['select'] = 'price-low'
        return context


def leashes_category_view(request, *args, **kwargs):
    """
    Collects context for page displaying Products in Leashes category
    No class based views for categories as pagination is not needed,
    not enough products to need to paginate.
    """
    if request.method == 'POST':
        context = get_post_request_context(request, 'Leashes')
        return render(request, "results.html", context)

    context = get_context('Leashes')
    return render(request, "results.html", context)


def collars_category_view(request, *args, **kwargs):
    """
    Collects context for page displaying Products in the Collars category.
    """
    if request.method == 'POST':
        context = get_post_request_context(request, 'Collars')
        return render(request, "results.html", context)

    context = get_context('Collars')
    return render(request, "results.html", context)


def beds_category_view(request, *args, **kwargs):
    """
    Collects context for page displaying Products in the Beds category.
    """
    if request.method == 'POST':
        context = get_post_request_context(request, 'Beds')
        return render(request, "results.html", context)

    context = get_context('Beds')
    return render(request, "results.html", context)


def carriers_category_view(request, *args, **kwargs):
    """
    Collects context for page displaying Products in Carriers category.
    """
    if request.method == 'POST':
        context = get_post_request_context(request, 'Carriers')
        return render(request, "results.html", context)

    context = get_context('Carriers')
    return render(request, "results.html", context)


def feeding_category_view(request, *args, **kwargs):
    """
    Collects context for page displaying Products in the Feeding category.
    """
    if request.method == 'POST':
        context = get_post_request_context(request, 'Feeding')
        return render(request, "results.html", context)

    context = get_context('Feeding')
    return render(request, "results.html", context)


def harnesses_category_view(request, *args, **kwargs):
    """
    Collects context for page displaying Products in the Harnesses category.
    """
    if request.method == 'POST':
        context = get_post_request_context(request, 'Harnesses')
        return render(request, "results.html", context)

    context = get_context('Harnesses')
    return render(request, "results.html", context)


def toys_category_view(request, *args, **kwargs):
    """
    Collects context for page displaying Products in the Toys category.
    """
    if request.method == 'POST':
        context = get_post_request_context(request, 'Toys')
        return render(request, "results.html", context)

    context = get_context('Toys')
    return render(request, "results.html", context)


def get_post_request_context(post_request, category_name):
    """
    Takes request and the relevant category name, and pulls the
    necessary context to fit the filer the user selected.
    """
    sort = post_request.POST.get('results-sort-select')
    if sort == 'price-high':
        results = Product.objects.all().filter(
            category=category_name).order_by('-price')
    elif sort == 'price-low':
        results = Product.objects.all().filter(category=category_name).order_by('price')
    elif sort == 'featured':
        featured = Product.objects.filter(
            category=category_name, featured=True)
        not_featured = Product.objects.filter(
            category=category_name, featured=False)
        results = list(chain(featured, not_featured))

    context = {
        'products': results,
        'select': sort,
        'category': category_name
    }
    return context


def get_context(category_name):
    """ Returns relevant context for category views """

    context = {
        'products': Product.objects.all().filter(category=category_name),
        'category': category_name
    }
    return context

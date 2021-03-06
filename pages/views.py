from django.shortcuts import render
from products.models import Product
from django.conf import settings
from .forms import ContactForm


# Create your views here.
def home_view(request, *args, **kwargs):
    """ Renders home page with 6 random
    featured products in featured listing section """

    featured_products = Product.objects.filter(featured=True).order_by('?')[:6]
    context = {
        'featured_products': featured_products,
        'category': 'All Products',
        'page': 'home',
    }
    return render(request, "index.html", context)


def about_view(request, *args, **kwargs):
    return render(request, "about.html", {"page": "about"})


def contact_view(request, *args, **kwargs):
    """
    Renders contact form on contact page
    with any relevant information the user has
    already provided in the name and email fields.
    """

    if request.user.is_authenticated:
        initial_data = {
            'name': request.user.first_name,
            'email': request.user.email
        }

        contact_form = ContactForm(initial=initial_data)

    else:
        contact_form = ContactForm()

    emailjs_user_id = settings.EMAILJS_USER_ID

    context = {
        "page": "contact",
        "form": contact_form,
        "emailjs_user_id": emailjs_user_id
    }

    return render(request, "contact.html", context)

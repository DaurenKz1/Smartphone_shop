from django.shortcuts import render
from .models import Brand
from cart.cart import Cart


def sidebar(request):
    brands = Brand.objects.all()
    context = {
        "brn": brands
    }
    return context


def cart(request):
    cart = Cart(request)
    context = {
        "cart": cart
    }
    return context



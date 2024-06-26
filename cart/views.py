from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Smartphone
from .cart import Cart
from django.contrib import messages


def cart_add(request, smartphoneid):
	cart = Cart(request)
	smartphone = get_object_or_404(Smartphone, id=smartphoneid)
	cart.add(smartphone=smartphone)

	return redirect('store:index')


def cart_update(request, smartphoneid, quantity):
	cart = Cart(request)
	smartphone = get_object_or_404(Smartphone, id=smartphoneid)

	if smartphone.stock >= int(quantity):
		cart.update(smartphone=smartphone, quantity=quantity)
		price = smartphone.price * int(quantity)
		return render(request, 'cart/price.html', {"price": price})
	else:
		messages.error(request, "На складе недостаточно смартфонов.")
		return HttpResponse(status=400)



def cart_remove(request, smartphoneid):
    cart = Cart(request)
    smartphone = get_object_or_404(Smartphone, id=smartphoneid)
    cart.remove(smartphone)
    return redirect('cart:cart_details')

def total_cart(request):
	return render(request, 'cart/totalcart.html')

def cart_summary(request):

	return render(request, 'cart/summary.html')

def cart_details(request):
	cart = Cart(request)
	context = {
		"cart": cart,
	}
	return render(request, 'cart/cart.html', context)


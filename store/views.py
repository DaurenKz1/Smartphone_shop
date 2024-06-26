from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Brand, Category, Smartphone, Review
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import RegistrationForm, ReviewForm


def index(request):
    new_smartphones = Smartphone.objects.order_by('-created_at')[:15]
    best_smartphones = Smartphone.objects.order_by('-totalrating')
    context = {
        "new_smartphones": new_smartphones,
        "best_smartphones": best_smartphones,
    }
    return render(request, 'store/index.html', context)


def signin(request):
    if request.user.is_authenticated:
        return redirect('store:index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('store:index')
            else:
                messages.error(request, 'Имя пользователя и пароль не совпадают.')

    return render(request, "store/login.html")


def signout(request):
    logout(request)
    return redirect('store:index')



def registration(request):
    if request.user.is_authenticated:
        return redirect('store:index')

    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']


            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Аккаунт был создан успешно")
                return redirect('store:index')
            else:
                messages.error(request, "Не удалось войти в систему после регистрации.")
        else:
            for error in form.errors.values():
                messages.error(request, error)

    return render(request, 'store/signup.html', {"form": form})



def payment(request):
    return render(request, 'store/payment.html')


def get_smartphone(request, id):
    form = ReviewForm(request.POST or None)
    smartphone = get_object_or_404(Smartphone, id=id)
    related_smartphones = Smartphone.objects.filter(category_id=smartphone.category.id)
    related_reviews = Review.objects.filter(smartphone_id=id).order_by('created')

    paginator = Paginator(related_reviews, 4)
    page = request.GET.get('page')
    r_review = paginator.get_page(page)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                temp = form.save(commit=False)
                temp.customer = User.objects.get(id=request.user.id)
                temp.smartphone = smartphone

                temp = Smartphone.objects.get(id=id)
                temp.totalreview += 1
                temp.totalrating += int(request.POST.get('review_star'))
                temp.save()
                form.save()
                messages.success(request, "Отзыв успешно добавлен.")
                form = ReviewForm()
        else:
            messages.error(request, "Сначала вам нужно войти в систему.")

    context = {
        "smartphone": smartphone,
        "related_smartphones": related_smartphones,
        "form": form,
        "related_reviews": r_review
    }
    return render(request, "store/smartphone.html", context)



def get_smartphones(request):
    smartphones_ = Smartphone.objects.all().order_by('created_at')
    paginator = Paginator(smartphones_, 5)
    page_number = request.GET.get('page')
    smartphones = paginator.get_page(page_number)
    return render(request, "store/brand.html", {"smartphone": smartphones})

def get_smartphone_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    smartphone_ = Smartphone.objects.filter(brand_id=id)
    paginator = Paginator(smartphone_, 10)
    page_number = request.GET.get('page')
    smartphone = paginator.get_page(page_number)
    return render(request, "store/brand.html", {"smartphone": smartphone, "brand": brand})


def get_category(request, id):
    category = get_object_or_404(Category, id=id)
    smartphones = Smartphone.objects.filter(brand_id=category.id)
    context = {
        "category": category,
        "smartphones": smartphones
    }
    return render(request, "store/brand.html", context)

def contact(request):
    return render(request, 'store/contact.html')
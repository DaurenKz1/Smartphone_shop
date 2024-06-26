from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from store.models import Smartphone

def search(request):
    search = request.GET.get('q')
    smartphone = Smartphone.objects.all()
    if search:
        smartphone = smartphone.filter(
            Q(name__icontains=search) |
            Q(category__name__icontains=search) |
            Q(brand__name__icontains=search)
        )

    paginator = Paginator(smartphone, 10)
    page = request.GET.get('page')
    smartphone = paginator.get_page(page)

    context = {
        'smartphone': smartphone,
        'search_query': search,
    }
    return render(request, 'store/brand.html', context)

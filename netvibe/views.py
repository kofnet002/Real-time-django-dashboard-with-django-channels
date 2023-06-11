from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, DataItem
from faker import Faker
from django.db.models import Sum
from django.http import JsonResponse

fake = Faker()

# Create your views here.


def main(request):
    qs = Statistic.objects.all()
    if request.method == 'POST':
        new_stat = request.POST.get('new-statistic')
        obj, _ = Statistic.objects.get_or_create(name=new_stat)
        return redirect(f'/{obj.slug}')

    context = {
        'qs': qs,
    }
    return render(request, 'netvibe/main.html', context)


def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)

    context = {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name
    }

    return render(request, 'netvibe/dashboard.html', context)


def chat_data(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    qs = obj.data.values('owner').annotate(Sum('value'))
    chart_data = [x["value__sum"] for x in qs]
    chart_labels = [x["owner"] for x in qs]
    return JsonResponse({
        "chartData": chart_data,
        "chartLabels": chart_labels,
    })

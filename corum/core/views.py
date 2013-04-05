# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from core.models import Case
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    all_cases = Case.objects.filter(parent_case=None)
    paginator = Paginator(all_cases, 2)
    page = request.GET.get('page')

    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)

    return render(request, 'cases.html', {'cases': cases})

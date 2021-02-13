from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

def home_page(request):
    # show home page of the whole website
    context = {'page': 'home'}
    return render(request, 'home_page.html', context)


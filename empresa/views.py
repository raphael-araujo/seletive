# from django.http import HttpResponse
from django.shortcuts import redirect, render,  HttpResponse


def nova_empresa(request):
    return render(request, 'nova_empresa.html')
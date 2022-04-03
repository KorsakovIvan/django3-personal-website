from django.shortcuts import render
from .models import Project


def home(request):
    projects = Project.objects.all()
    return render(request, 'website/home.html', {'projects': projects})

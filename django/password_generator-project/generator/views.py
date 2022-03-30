from django.shortcuts import render
from django.http import HttpResponse
import random


# Create your views here.
def home(request):
    return render(request, 'generator/home.html')


def about(request):
    return render(request, 'generator/about.html')


def password(request):
    characters = list('abcdefghijklmnopqrstuvwxyz')
    length = int(request.GET.get('length', 12))

    include_uppercase = bool(request.GET.get('uppercase', False))
    if include_uppercase:
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    include_special = bool(request.GET.get('special', False))
    if include_special:
        characters.extend(list('±§!@#$%^&*()_-+=/.><,;:{}][`~'))

    include_numbers = bool(request.GET.get('numbers', False))
    if include_numbers:
        characters.extend(list('1234567890'))

    the_password = ''
    for x in range(length):
        the_password += random.choice(characters)

    return render(request, 'generator/password.html', {'password': the_password})

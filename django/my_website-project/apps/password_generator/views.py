from django.shortcuts import render
import random


def home(request):
    return render(request, 'password_generator/home.html')


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

    return render(request, 'password_generator/password_generated.html', {'password': the_password})

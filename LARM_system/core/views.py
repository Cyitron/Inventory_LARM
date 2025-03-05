from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def cadastro_view(request):
    return render(request, 'cadastro.html')

def main_menu(request):
    return render(request, 'main_menu.html')
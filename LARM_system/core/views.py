from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def cadastro_view(request):
    return render(request, 'cadastro.html')

def main_menu(request):
    # Verifica se o usuário está autenticado e se é administrador.
    is_admin = request.user.is_authenticated and request.user.is_staff
    return render(request, 'main_menu.html', {'is_admin': is_admin})

def inventario(request):
    return render(request, 'inventario.html')

def admin_cadastro(request):
    return render(request, "admin-cadastro.html")
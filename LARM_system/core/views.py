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

from django.shortcuts import render
from .models import MaterialConsumo, MaterialPermanente

def estoque_atual(request):
    materiais_consumo = MaterialConsumo.objects.select_related('id_item').all()
    materiais_permanentes = MaterialPermanente.objects.select_related('id_item').all()
    return render(request, 'estoque.html', {
        'materiais_consumo': materiais_consumo,
        'materiais_permanentes': materiais_permanentes
    })

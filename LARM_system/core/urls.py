from django.urls import path
from .views import login_view, cadastro_view, main_menu, inventario, admin_cadastro

urlpatterns = [
    path('login/', login_view, name='login'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('menu/', main_menu, name="main_menu"),
    path('inventario/', inventario, name="inventario"),
    path('admin-cadastro/', admin_cadastro, name="admin-cadastro")
]
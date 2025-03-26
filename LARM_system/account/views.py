from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Account  # Certifique-se de que este é o modelo correto
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def cadastrar_usuario(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        tipo_usuario = request.POST.get("tipo_usuario")
        
        matricula = request.POST.get("matricula", "")
        curso = request.POST.get("curso", "")
        siape = request.POST.get("siape", "")
        departamento = request.POST.get("departamento", "")

        # Definir o username e a senha
        if tipo_usuario == "aluno":
            username = nome  # O username será o nome completo
            password = matricula
        elif tipo_usuario in ["servidor", "professor"]:
            username = nome
            password = siape
        else:  # Externo
            username = nome
            password = email

        # Criar o usuário Django
        usuario = User.objects.create_user(username=username, password=password)
        usuario.save()

        # Criar perfil adicional
        account = Account.objects.create(
            user=usuario,
            telefone=telefone,
            tipo_usuario=tipo_usuario,
            nome=usuario,
            matricula=matricula if tipo_usuario == "aluno" else None,
            curso=curso if tipo_usuario == "aluno" else None,
            siape=siape if tipo_usuario in ["servidor", "professor"] else None,
            departamento=departamento if tipo_usuario == "professor" else None,
        )
        account.save()

        messages.success(request, "Cadastro realizado com sucesso! Aguarde aprovação do administrador.")
        return redirect("login")  # Redireciona para a página de login

    return render(request, "cadastro.html")

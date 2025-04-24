from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from core import models


@csrf_exempt
def cadastrar_usuario(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        tipo_usuario = request.POST.get("tipo_usuario")

        # Campos específicos
        matricula = request.POST.get("matricula")
        curso = request.POST.get("curso")
        siape = request.POST.get("siape")
        departamento = request.POST.get("departamento")

        # Determina a senha com base no tipo
        if tipo_usuario == "aluno":
            senha = matricula
        elif tipo_usuario in ["servidor", "professor"]:
            senha = siape
        elif tipo_usuario == "externo":
            senha = email
        else:
            senha = "senha_padrao"

        senha = make_password(senha)

        # Criação do usuário
        novo_usuario = models.Usuario.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            tipo_user={
                'aluno': 1,
                'servidor': 2,
                'professor': 3,
                'externo': 4
            }.get(tipo_usuario, None),
            is_active=False,
            data_aprovacao=None,
            password=senha
        )

        # Inserir dados extras conforme o tipo
        if tipo_usuario == "aluno":
            models.Aluno.objects.create(
                matricula=int(matricula),
                curso=curso,
                id_user=novo_usuario
            )

        elif tipo_usuario == "servidor":
            models.Servidor.objects.create(
                siare=int(siape),
                id_user=novo_usuario
            )

        elif tipo_usuario == "professor":
            departamento_obj, _ = models.Departamento.objects.get_or_create(
                nome_departamento=departamento
            )
            models.Professor.objects.create(
                siare=int(siape),
                id_user=novo_usuario,
                id_departamento=departamento_obj
            )

        messages.success(request, "Pedido de cadastro enviado com sucesso! Aguarde aprovação.")
        return redirect("home")

    return render(request, "cadastro.html")

def admin_cadastro(request):
    if request.method == "POST":
        # Atualização de ativação/inativação
        user_id = request.POST.get("user_id")
        is_active = request.POST.get("is_active") == "on"

        usuario = models.Usuario.objects.get(id_user=user_id)
        usuario.is_active = is_active
        usuario.save()

        # Atualizar permissões
        todas_permissoes = models.Permicao.objects.all()
        models.Permicoes.objects.filter(id_user=usuario).delete()

        for perm in todas_permissoes:
            if request.POST.get(f"perm_{perm.id_permicao}") == "on":
                models.Permicoes.objects.create(
                    id_user=usuario,
                    id_permicao=perm
                )

        return redirect("admin-cadastro")

    usuarios = models.Usuario.objects.all()
    permissoes = models.Permicao.objects.all()
    permissoes_ativas = {
        p.id_user.id_user: set(
            models.Permicoes.objects.filter(id_user=p.id_user).values_list('id_permicao__id_permicao', flat=True)
        )
        for p in models.Permicoes.objects.select_related('id_user')
    }

    return render(request, "admin-cadastro.html", {
        "usuarios": usuarios,
        "permissoes": permissoes,
        "permissoes_ativas": permissoes_ativas
    })
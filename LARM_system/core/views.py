from django.shortcuts import render, redirect
from .models import MaterialConsumo, MaterialPermanente, Usuario, Permicao, Permicoes
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        try:
            user = Usuario.objects.get(nome=username)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuário ou senha inválidos.")
            return render(request, "login.html")

        if not user.is_active:
            messages.error(request, "Usuário inativo. Aguarde aprovação do administrador.")
            return render(request, "login.html")

        if not check_password(password, user.password):
            messages.error(request, "Usuário ou senha inválidos.")
            return render(request, "login.html")

        # Autenticação bem-sucedida: salva na sessão
        request.session["user_id"] = user.id_user
        request.session.set_expiry(3600)  # 1 hora
        return redirect("main_menu")

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')

def cadastro_view(request):
    return render(request, 'cadastro.html')

#def main_menu(request):
    # Verifica se o usuário está autenticado e se é administrador.
    #is_admin = request.user.is_authenticated and request.user.is_staff
#    return render(request, 'main_menu.html') #{'is_admin': is_admin})
def main_menu(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    usuario = Usuario.objects.get(id_user=user_id)

    # Busca IDs de permissão ativas para este usuário
    permissoes_ativas = Permicoes.objects.filter(
        id_user=usuario, permicao_active=True
    ).values_list('id_permicao__id_permicao', flat=True)
    permissoes_ativas = set(permissoes_ativas)

    # Só habilita se tiver permissão 2 (inventário) e 1 (cadastro/admin)
    can_inventario = 2 in permissoes_ativas
    can_cadastro   = 1 in permissoes_ativas
    # can_delete = 3 in permissoes_ativas

    return render(request, "main_menu.html", {
        "usuario": usuario,
        "can_inventario": can_inventario,
        "can_cadastro":   can_cadastro,
    })

def inventario(request):
    user_id = request.session.get("user_id")
    # if not user_id:
    #     return redirect("login")
    
    usuario = Usuario.objects.get(id_user=user_id)

    # Busca IDs de permissão ativas para este usuário
    permissoes_ativas = Permicoes.objects.filter(
        id_user=usuario, permicao_active=True
    ).values_list('id_permicao__id_permicao', flat=True)
    permissoes_ativas = set(permissoes_ativas)

    can_report = 3 in permissoes_ativas
    can_inventario = 2 in permissoes_ativas

    return render(request, 'inventario.html', {
        "usuario": usuario,
        "can_inventario:": can_inventario,
        "can_report": can_report
    })

@csrf_exempt
def admin_cadastro(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        is_active = request.POST.get("is_active") == "on"

        # Atualiza o usuário
        usuario = Usuario.objects.get(id_user=user_id)
        usuario.is_active = is_active
        usuario.save()

        # Atualiza cada permissão
        for perm in Permicao.objects.all():
            field = f"perm_{perm.id_permicao}"
            ativo = field in request.POST
            rel, created = Permicoes.objects.get_or_create(
                id_user=usuario,
                id_permicao=perm,
                defaults={'permicao_active': ativo}
            )
            if not created:
                rel.permicao_active = ativo
                rel.save()

        return redirect("admin-cadastro")

    # GET: montar lista de usuários com seu set de permissões ativas
    usuarios = list(Usuario.objects.all())
    # busca apenas as relações ativas
    rels = Permicoes.objects.filter(permicao_active=True).select_related('id_user', 'id_permicao')
    # dicionário user_id -> set(perm_id)
    mapa = {}
    for r in rels:
        mapa.setdefault(r.id_user.id_user, set()).add(r.id_permicao.id_permicao)

    # anexa atributo .active_perms a cada usuário
    for u in usuarios:
        u.active_perms = mapa.get(u.id_user, set())

    return render(request, 'admin-cadastro.html', {
        'usuarios': usuarios,
        'permissoes': Permicao.objects.all(),
    })


def estoque_atual(request):
    materiais_consumo = MaterialConsumo.objects.select_related('id_item').all()
    materiais_permanentes = MaterialPermanente.objects.select_related('id_item').all()
    return render(request, 'estoque.html', {
        'materiais_consumo': materiais_consumo,
        'materiais_permanentes': materiais_permanentes
    })

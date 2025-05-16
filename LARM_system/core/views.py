from django.shortcuts import render, redirect
from .models import MaterialConsumo, MaterialPermanente, Usuario, Permicao, Permicoes, Item
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import pandas as pd
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

def cadastro_item_perm(request):
    if request.method == "POST":
        # Só processa o envio de Excel
        if request.POST.get("acao") == "importar_excel" and request.FILES.get("arquivo"):
            arquivo = request.FILES["arquivo"]
            try:
                # 1) Lê planilha sem header
                df_raw = pd.read_excel(arquivo, engine="openpyxl", header=None)

                # 2) Encontra a linha que menciona "LARM"
                mask = df_raw.apply(lambda col: col.astype(str).str.contains("LARM", na=False)).any(axis=1)
                if not mask.any():
                    messages.error(request, "Não foi encontrada a seção LARM no arquivo.")
                    return redirect("cadastro_item_perm")
                idx_larm = mask[mask].index[0]

                # 3) Cabeçalho está duas linhas abaixo
                idx_header = idx_larm + 2
                df_raw.columns = df_raw.iloc[idx_header]

                # DEBUG: imprima os cabeçalhos para ver exatamente os nomes
                print("=== CABEÇALHOS DETECTADOS ===")
                for col in df_raw.columns:
                    print(f"'{col}'")

                # 4) Dados reais começam na linha seguinte
                df = df_raw.iloc[idx_header+1:].copy()

                # 5) Filtra linhas até encontrar a primeira linha em branco na coluna chave
                df = df[df['Material'].notna()]

                inseridos = 0
                ignorados = 0

                # 6) Itera apenas pelas colunas que precisamos
                for _, row in df.iterrows():
                    legado = row.to_dict()
                    try:
                        patrimonio = legado.get("Cód. barras")
                        if patrimonio is None:
                            patrimonio = 0
                            continue
                        descricao  = legado.get("Material")
                        situacao   = legado.get("Situação")
                        valor      = legado.get("Valor (R$)")


                        # Validações básicas
                        if pd.isna(patrimonio) or pd.isna(descricao):
                            ignorados += 1
                            continue
                        patrimonio = int(patrimonio)

                        # Evita duplicatas
                        if MaterialPermanente.objects.filter(id_patrimonio=patrimonio).exists():
                            ignorados += 1
                            continue

                        # Criação
                        item = Item.objects.create(
                            descricao=descricao,
                            tipo="permanente"
                        )
                        MaterialPermanente.objects.create(
                            id_item=item,
                            valor=float(valor) if pd.notna(valor) else None,
                            id_patrimonio=patrimonio,
                            situacao=situacao if pd.notna(situacao) else None,
                            data_registro=datetime.now().date()
                        )
                        inseridos += 1

                    except Exception:
                        ignorados += 1
                        continue

                messages.success(
                    request,
                    f"Importação concluída: {inseridos} itens inseridos, {ignorados} ignorados."
                )
                return redirect("estoque_atual")

            except Exception as e:
                messages.error(request, f"Erro ao processar arquivo: {e}")
                return redirect("cadastro_item_perm")

        # Formulário individual de cadastro
        else:
            descricao = request.POST.get("descricao")
            valor = request.POST.get("valor")
            patrimonio = request.POST.get("id_patrimonio")
            situacao = request.POST.get("situacao")
            data_baixa = request.POST.get("data_baixa")

            item = Item.objects.create(
                descricao=descricao,
                tipo="permanente"
            )

            MaterialPermanente.objects.create(
                id_item=item,
                valor=float(valor),
                id_patrimonio=int(patrimonio),
                situacao=situacao,
                data_baixa=data_baixa if data_baixa else None,
                data_registro=datetime.now().date()
            )

            messages.success(request, "Item permanente cadastrado com sucesso!")
            return redirect("cadastro_item_perm")

    return render(request, "cadastro_item_perm.html")

def cadastro_item_cons(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        qtd = int(request.POST.get('qtd'))
        valor = float(request.POST.get('valor'))

        # Cria o item com tipo fixo
        novo_item = Item.objects.create(descricao=descricao, tipo='Consumo')

        # Cria o material de consumo vinculado
        MaterialConsumo.objects.create(
            id_item=novo_item,
            qtd=qtd,
            valor=valor,
            data_registro=timezone.now().date()
        )

        return redirect('inventario')

    return render(request, 'cadastro_item_cons.html')
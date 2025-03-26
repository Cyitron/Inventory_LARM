from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos obrigatórios do usuario preencher
    tipo_usuario = models.CharField(
        "Vinculo",
        max_length= 9,
        choices=[
            ('aluno', 'Aluno'),
            ('professor','Professor'),
            ('servidor','Servidor'),
            ('externo', 'Externo')
        ],
        default='aluno'
    )

    nome = models.CharField(
        "Nome Completo",
        max_length=100,
        default='fulano'
    )

    email = models.EmailField(
        "E-mail",
        unique=True,
        default='default@default.com'
    )

    telefone = models.CharField(
        "Telefone",
        unique=True,
        max_length=15,
        default='(999)99999-9999'
    )

    # foto opcional por enquanto
    foto = models.ImageField(
        "Foto",
        upload_to="perfil_fotos/",
        blank=True,
        null=True
    )

    # campos que deverão ser preechidos dependendo do vinculo do inscrito
    curso = models.CharField(
        "Curso",
        max_length=4,
        choices=[
            ('ENC', 'ENC'),
            ('ENE', 'ENE'),
            ('TIC', 'TIC'),
            ('MED', 'MED'),
            ('FT', 'FT')
        ],
        blank=True,
        null=True
    )

    departamento = models.CharField(
        "Departamento",
        max_length=4,
        choices=[
            ('DEC', 'DEC'),
            ('CIT', 'CIT'),
            ('DCM', 'DCM'),
            ('DCS', 'DCS'),
            ('DFT', 'DFT'),
            ('EES', 'EES'),
            ('FQM', 'FQM')
        ],
        blank=True,
        null=True
    )

    matricula = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    siape = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    # os campos abaixo serão preenchidos pelo sistema ou por um admin
    is_active = models.BooleanField(
        "Usuario ativo",
        default=False,
        choices=[
            (True, 'Sim'),
            (False, 'Não')
        ]
    )

    aprov_date = models.DateField(
        "data de aprovação",
        null=True,
        blank=True
    )

    enter_date = models.DateField(
        "data de inscrição",
        auto_now_add=True
    )
    
    # ===================================

    def __str__(self):
        return self.user.username
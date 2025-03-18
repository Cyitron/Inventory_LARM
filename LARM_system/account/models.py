from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    type_of_user = models.CharField(
        "Vinculo",
        max_length= 9,
        choices=[
            ('aluno', 'aluno'),
            ('professor','professor'),
            ('servidor','servidor'),
            ('externo', 'externo')
        ]
    )

    name = models.CharField(
        "Nome Completo",
        max_length=100,
    )

    email = models.EmailField(
        "E-mail",
        unique=True
    )

    cell_number = models.CharField(
        "(DDD)99999-9999",
        unique=True,
        max_length=15
    ) #(DDD)99999-9999

    photo = models.ImageField(
        "Foto",
        upload_to="perfil_fotos/",
        blank=True,
        null=True
    )

    course = models.CharField(
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

    departament = models.CharField(
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
    enter_date = models.DateField(
        "data de inscrição",
        auto_now_add=True
    )

    aprov_date = models.DateField(
        "data de aprovação",
        null=True,
        blank=True
    )
    
    # ===================================

    def __str__(self):
        return self.user.username
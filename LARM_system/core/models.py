# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    enter_date = models.DateField()
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)
    aprov_date = models.DateField(blank=True, null=True)
    curso = models.CharField(max_length=4, blank=True, null=True)
    departamento = models.CharField(max_length=4, blank=True, null=True)
    email = models.CharField(unique=True, max_length=254)
    matricula = models.CharField(max_length=10, blank=True, null=True)
    nome = models.CharField(max_length=100)
    foto = models.CharField(max_length=100, blank=True, null=True)
    siape = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField()
    telefone = models.CharField(unique=True, max_length=15)
    tipo_usuario = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'account_account'


class Aluno(models.Model):
    matricula = models.IntegerField(unique=True, blank=True, null=True)
    curso = models.TextField(blank=True, null=True)
    id_user = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aluno'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Consumo(models.Model):
    id_consumo = models.AutoField(primary_key=True)
    data_consumo = models.DateField(blank=True, null=True)
    motivo_uso = models.TextField(blank=True, null=True)
    qtd_consumida = models.IntegerField(blank=True, null=True)
    id_user = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consumo'


class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nome_departamento = models.TextField()

    class Meta:
        managed = False
        db_table = 'departamento'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Emprestimo(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    data_devolucao = models.DateField(blank=True, null=True)
    data_emprestimo = models.DateField()
    id_user = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emprestimo'


class Externo(models.Model):
    id_user = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_user', primary_key=True)  # The composite primary key (id_user, id_inst) found, that is not supported. The first column is selected.
    id_inst = models.ForeignKey('Instituicao', models.DO_NOTHING, db_column='id_inst')

    class Meta:
        managed = False
        db_table = 'externo'
        unique_together = (('id_user', 'id_inst'),)


class Instituicao(models.Model):
    id_inst = models.AutoField(primary_key=True)
    nome_inst = models.TextField()

    class Meta:
        managed = False
        db_table = 'instituicao'


class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    descricao = models.TextField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'


class MaterialConsumo(models.Model):
    id_item = models.OneToOneField(Item, models.DO_NOTHING, db_column='id_item', primary_key=True)
    qtd = models.IntegerField(blank=True, null=True)
    data_registro = models.DateField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_consumo'


class MaterialPermanente(models.Model):
    id_item = models.OneToOneField(Item, models.DO_NOTHING, db_column='id_item', primary_key=True)
    data_baixa = models.DateField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    id_patrimonio = models.TextField(unique=True, blank=True, null=True)
    situacao = models.TextField(blank=True, null=True)
    data_registro = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_permanente'


class Professor(models.Model):
    siare = models.IntegerField(unique=True, blank=True, null=True)
    id_user = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'professor'


class Servidor(models.Model):
    siare = models.IntegerField(unique=True, blank=True, null=True)
    id_user = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_user', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servidor'


class Usuario(models.Model):
    id_user = models.AutoField(primary_key=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)
    nome = models.TextField()
    data_aprovacao = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    tipo_user = models.IntegerField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'

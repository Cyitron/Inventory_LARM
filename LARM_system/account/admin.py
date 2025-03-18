from django.contrib import admin
from account.models import Account
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class AccountInLine(admin.StackedInline):
    model = Account
    can_delete = False # coloquei falso para nenhuma conta ser excluida sem excluir o usuario associado a ela (se excluir o usuario a account vai ser excluida)
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(Account)
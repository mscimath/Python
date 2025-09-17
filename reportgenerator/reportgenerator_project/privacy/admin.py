from django.contrib import admin

# Register your models here.
from .models import UserData

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('typ_danych', 'sektor', 'jurysdykcja', 'opis')

from django.contrib import admin

from core.models import Evento

# cria uma classe de representação para ser apresentada no Admin
class EventoAdmin(admin.ModelAdmin):
    # define os campos que devem ser apresentandos na lista do Admin
    list_display = ('titulo', 'data_evento', 'data_criacao')
    # cria uma lista de filtros 
    list_filter = ('titulo', 'usuario')

# Register your models here.
# adiciona o model e vincula o model a sua classe de representação
admin.site.register(Evento, EventoAdmin)
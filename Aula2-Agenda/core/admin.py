from django.contrib import admin
from core.models import Evento

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'data_criacao')
    list_filter = ('usuario', 'titulo', 'data_evento',) #a vírgula tem de estar no final, se ñ acontecerá um erro

admin.site.register(Evento, EventoAdmin)
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

#def index (request):
#    return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username') #recuperar o conteúdo do parâmetro 'username' na url submit_login
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None: #se o user ñ for vazio, é feito o login; e retornando ao índice '/'
            login(request, usuario)
            return redirect('/') #ao retornar p/ o índice ele vai passar pela validação do decorador required...
        else:
            messages.error(request, "Usuário ou senha inválido")
    return redirect('/')

@login_required(login_url='/login/') #qnd ñ tiver autenticado, é levado para tal endereço
def lista_eventos(request):
    usuario = request.user #pegando o user q está fzd a requisição, assim se consegue fazer uma consulta por ele
    evento = Evento.objects.filter(usuario=usuario) #mesma coisa do all, mas com parâmetro na filtragem, só vai retornar os eventos do usuario logado
    #evento = Evento.objects.all()
    dados = {'eventos':evento} #evento agora é no plural
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                           data_evento=data_evento,
            #                                           descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)  #na listagem era um objects.filter, aqui é um objects.create
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    #Evento.objects.filter(id=id_evento).delete() #vulnerável a users excluir registros q ñ são deles;
    evento = Evento.objects.get(id=id_evento) #agr, cada user só excluirá seus eventos
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')
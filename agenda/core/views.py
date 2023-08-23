from django.shortcuts import redirect, render
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

# página de login 
# não criar como nome do método login, pois já existe esse método
def login_user(request): 
    return render(request, 'login.html')

# rota de logout
def logout_user(request):
    # faz o logout
    logout(request)
    # redireciona para o índice após o logout
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # faz a autenticação
        usuario = authenticate(username=username, password=password)
        # se a autenticação for válida retorna valor
        if usuario is not None: 
            # após a autenticação ser válida é necessário criar a sessão com o login
            login(request, usuario)
            return redirect('/')        
        else:
            # se a autenticação é inválida coloca a mensagem de erro em uma lista
            messages.error(request, 'Usuário ou senha inválidos') 
    return redirect('/')

# a view só será exibida se o usuário estiver autenticado
# caso não esteja autenticado, rediciona para a página login (parametro opcional)
@login_required(login_url='/login/')
def lista_eventos(request):
    # recebe o usuário que esta logado
    usuario = request.user
    # retorna os objetos somente deste usuário 
    # faz um filtro
    evento = Evento.objects.filter(usuario = usuario)
    # cria um dicionário de response (dados)
    dados = { 'eventos' : evento }
    # o parametro response não é obrigatório
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    #pega o parametro da rota se existir
    id_evento = request.GET.get('id')
    dados = {}
    # carrega os dados do evento se o id foi informado
    if id_evento: 
        dados['evento'] = Evento.objects.get(id=id_evento) 
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        id_evento = request.POST.get('id_evento')
        usuario = request.user
        if id_evento:
            evento = Evento.objects.get(id = id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            # Outra forma de fazer o update, a forma acima é melhor pq valida o usuário
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            data_evento=data_evento, 
            #                                            descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo, 
                                  data_evento = data_evento, 
                                  descricao = descricao,   
                                  usuario = usuario)
    return redirect('/') 

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    evento = Evento.objects.get(id = id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')
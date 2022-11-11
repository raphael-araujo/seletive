from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import HttpResponse, redirect, render

from .models import Empresa, Tecnologia
from .utils import empresa_is_valid


def nova_empresa(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        cidade = request.POST['cidade']
        endereco = request.POST['endereco']
        nicho = request.POST['nicho']
        tecnologias = request.POST.getlist('tecnologias')
        caracteristicas = request.POST['caracteristicas']
        logo = request.FILES.get('logo')
        print(f'1- {tecnologias}')
        if not empresa_is_valid(request, nome, email, cidade, endereco, nicho, tecnologias, caracteristicas, logo):
            return redirect('/home/nova_empresa')
        try:
            e = Empresa(
                logo=logo,
                nome=nome,
                email=email,
                cidade=cidade,
                endereco=endereco,
                nicho_mercado=nicho,
                caracteristica_empresa=caracteristicas
            )
            e.save()
            e.tecnologias.add(*tecnologias)
            e.save()

            messages.add_message(
                request,
                level=constants.SUCCESS,
                message='Empresa cadastrada com sucesso.'
            )
            return redirect('/home/empresas')
        except:
            messages.add_message(
                request,
                level=constants.ERROR,
                message='Erro interno do sistema'
            )
            return redirect('/home/nova_empresa')

    else:
        techs = Tecnologia.objects.all()
        context = {
            'techs': techs
        }
        return render(request, 'nova_empresa.html', context)


def empresas(request):
    empresas = Empresa.objects.all()
    tecnologias = Tecnologia.objects.all()
    context = {
        'empresas': empresas,
        'tecnologias': tecnologias
    }

    return render(request, 'empresas.html', context)
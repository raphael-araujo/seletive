from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

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
    filtro_nome = request.GET.get('nome')
    filtro_tecnologia = request.GET.get('tecnologias')
    empresas = Empresa.objects.all()
    tecnologias = Tecnologia.objects.all()

    if filtro_nome:
        empresas = Empresa.objects.filter(nome__icontains=filtro_nome)

    if filtro_tecnologia:
        empresas = Empresa.objects.filter(tecnologias=filtro_tecnologia)

    context = {
        'empresas': empresas,
        'tecnologias': tecnologias
    }

    return render(request, 'empresas.html', context)


def excluir_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    empresa.delete()
    
    messages.add_message(
        request,
        level=constants.WARNING,
        message=f'Empresa "{empresa.nome}" excluída com sucesso.'
    )
    return redirect('/home/empresas')
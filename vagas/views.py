from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from django.shortcuts import redirect, render
from empresa.models import Vaga

from .utils import vaga_is_valid


def nova_vaga(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        email = request.POST['email']
        tecnologias_dominadas = request.POST.getlist('tecnologias_domina')
        tecnologias_nao_dominadas = request.POST.getlist('tecnologias_nao_domina')
        experiencia = request.POST['experiencia']
        data_final = request.POST['data_final']
        empresa = request.POST['empresa']
        status = request.POST['status']

        if not vaga_is_valid(request, titulo, email, tecnologias_dominadas, tecnologias_nao_dominadas, experiencia, data_final, empresa, status):
            return redirect(f'/home/empresa/{empresa}')

        try:
            v = Vaga(
                empresa_id=empresa,
                titulo=titulo,
                email=email,
                nivel_experiencia=experiencia,
                data_final=data_final,
                status=status
            )
            v.save()

            v.tecnologias_dominadas.add(*tecnologias_dominadas)
            v.tecnologias_estudar.add(*tecnologias_nao_dominadas)
            v.save()

            messages.add_message(
                request,
                constants.SUCCESS,
                message='Vaga criada com sucesso.'
            )
            return redirect(f'/home/empresa/{empresa}')
        except:
            messages.add_message(
                request,
                constants.ERROR,
                message='Erro interno do sistema.'
            )
            return redirect(f'/home/empresa/{empresa}')
    else:
        raise Http404()

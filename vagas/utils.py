from django.contrib import messages
from django.contrib.messages import constants


def vaga_is_valid(request, titulo, email, tecnologias_dominadas, tecnologias_nao_dominadas, experiencia, data_final, empresa, status):
    from empresa.models import Empresa, Vaga

    empresas = Empresa.objects.all()

    if (len(titulo.strip()) == 0) or (len(email.strip()) == 0) or (len(tecnologias_dominadas) == 0) or (len(tecnologias_nao_dominadas) == 0) or (len(experiencia.strip()) == 0) or (len(data_final) == 0) or (len(empresa.strip()) == 0) or (len(status.strip()) == 0):
        messages.add_message(
            request,
            level=constants.ERROR,
            message='Preencha todos os campos.'
        )
        return False

    if experiencia not in [i[0] for i in Vaga.choices_experiencia]:
        messages.add_message(
            request,
            level=constants.ERROR,
            message='Nível de experiência inválido'
        )
        return False

    if int(empresa) not in [i.id for i in empresas]:
        messages.add_message(
            request,
            level=constants.ERROR,
            message='A empresa selecionada não existe'
        )
        return False

    if status not in [i[0] for i in Vaga.choices_status]:
        messages.add_message(
            request,
            level=constants.ERROR,
            message='Status inválido'
        )
        return False

    return True


def tarefa_is_valid(request, titulo, prioridade, data):
    from .models import Tarefa

    if (len(titulo.strip()) == 0) or (len(prioridade.strip()) == 0) or (len(data.strip()) == 0):
        messages.add_message(
            request,
            level=constants.ERROR,
            message='Preencha todos os campos.'
        )
        return False

    if prioridade not in [i[0] for i in Tarefa.choices_prioridade]:
        messages.add_message(
            request,
            level=constants.ERROR,
            message='Nível de prioridade inválido.'
        )
        return False

    return True

from django.contrib import messages
from django.contrib.messages import constants


def empresa_is_valid(request, nome, email, cidade, endereco, nicho, tecnologias, caracteristicas, logo):
    from .models import Empresa

    if (len(nome.strip()) == 0) or (len(email.strip()) == 0) or (len(cidade.strip()) == 0) or (len(endereco.strip()) == 0) or (len(nicho.strip()) == 0) or (len(tecnologias) == 0) or (len(caracteristicas.strip()) == 0) or (not logo):
        messages.add_message(
            request,
            level=constants.ERROR,
            message='Preencha todos os campos.'
        )
        return False

    if logo.size > 100_000_000:
        messages.add_message(
            request,
            level=constants.ERROR,
            message='A logo da empresa deve ter menos de 10MB.'
        )
        return False

    if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
        messages.add_message(
            request,
            level=constants.ERROR,
            message='Nicho de mercado inválido.'
        )
        return False

    return True

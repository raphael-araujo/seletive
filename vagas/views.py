from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from empresa.models import Vaga

from .models import Emails, Tarefa
from .utils import enviar_email_is_valid, tarefa_is_valid, vaga_is_valid


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


def vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)
    tarefas = Tarefa.objects.filter(vaga=vaga).filter(realizada=False)
    emails = Emails.objects.filter(vaga=vaga)

    context = {
        'vaga': vaga,
        'tarefas': tarefas,
        'emails': emails
    }

    return render(request, 'vaga.html', context)


def nova_tarefa(request, id_vaga):
    titulo = request.POST['titulo']
    prioridade = request.POST['prioridade']
    data = request.POST['data']

    if not tarefa_is_valid(request, titulo, prioridade, data):
        return redirect(f'/vagas/vaga/{id_vaga}')

    try:
        t = Tarefa(
            vaga_id=id_vaga,
            titulo=titulo, 
            prioridade=prioridade,
            data=data
        )
        t.save()

        messages.add_message(
            request,
            constants.SUCCESS,
            message='Tarefa adicionada com sucesso.'
        )
        return redirect(f'/vagas/vaga/{id_vaga}')

    except:
        messages.add_message(
            request,
            constants.ERROR,
            message='Erro interno do sistema'
        )
        return redirect(f'/vagas/vaga/{id_vaga}')


def finalizar_tarefa(request, id):
    tarefas_list = Tarefa.objects.filter(id=id).filter(realizada=False)

    if not tarefas_list.exists():
        messages.add_message(
            request,
            constants.ERROR,
            message='Erro interno do sistema'
        )
        return redirect('/home/empresas/')

    tarefa = tarefas_list.first()
    tarefa.realizada = True
    tarefa.save()

    messages.add_message(
        request,
        constants.SUCCESS,
        message='Tarefa finalizada com sucesso.'
    )
    return redirect(f'/vagas/vaga/{tarefa.vaga.id}')


def enviar_email(request, id_vaga):
    vaga = get_object_or_404(Vaga, id=id_vaga)
    assunto = request.POST['assunto']
    corpo = request.POST['corpo']

    html_content = render_to_string('emails/template_email.html', {'corpo': corpo})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, [vaga.email,])
    email.attach_alternative(html_content, 'text/html')

    if not enviar_email_is_valid(request, assunto, corpo):
        return redirect(f'/vagas/vaga/{id_vaga}')
    try:
        if email.send():
            mail = Emails(
                vaga=vaga,
                assunto=assunto,
                corpo=corpo,
                enviado=True
            )
            mail.save()

            messages.add_message(
                request,
                constants.SUCCESS,
                message='Email enviado com sucesso.'
            )
            return redirect(f'/vagas/vaga/{id_vaga}')
    except:
        mail = Emails(
            vaga=vaga,
            assunto=assunto,
            corpo=corpo,
            enviado=False
        )
        mail.save()

        messages.add_message(
            request,
            constants.ERROR,
            message='Erro interno do sistema.'
        )
        return redirect(f'/vagas/vaga/{id_vaga}')

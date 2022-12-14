from django.urls import path
from . import views

urlpatterns = [
    path('nova_vaga/', views.nova_vaga, name='nova_vaga'),
    path('vaga/<int:id>', views.vaga, name='vaga'),
    path('atualizar_progresso/<int:id_vaga>', views.atualizar_progresso, name='atualizar_progresso'),
    path('nova_tarefa/<int:id_vaga>', views.nova_tarefa, name='nova_tarefa'),
    path('finalizar_tarefa/<int:id>', views.finalizar_tarefa, name='finalizar_tarefa'),
    path('enviar_email/<int:id_vaga>', views.enviar_email, name='enviar_email'),
    path('tecnologia_status/<int:id_vaga>', views.tecnologia_status, name='tecnologia_status')
]

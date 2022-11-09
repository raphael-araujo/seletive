from django.contrib import admin

from .models import Empresa, Tecnologia, Vaga

admin.site.register(Empresa)
admin.site.register(Tecnologia)
admin.site.register(Vaga)
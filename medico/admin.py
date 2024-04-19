from django.contrib import admin
from . models import Especialidades, DadosMedico, DatasAbertas



class EspecialidadesAdmin(admin.ModelAdmin):
    list_display = ('id','especialidade',)


admin.site.register(Especialidades, EspecialidadesAdmin)
admin.site.register(DadosMedico)
admin.site.register(DatasAbertas)



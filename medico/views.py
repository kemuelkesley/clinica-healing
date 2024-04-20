from django.shortcuts import redirect, render
from .models import Especialidades, DadosMedico, is_medico, DatasAbertas
from paciente.models import Consulta
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


# Cadastrando médico

@login_required
def cadastro_medico(request):

    # Dados do médico
    # dm = DadosMedico.objects.filter(user=request.user)
    # if dm.exists():
    #     messages.add_message(request, constants.WARNING, 'Você já é médico.')
    #     return redirect('/medicos/abrir_horario')

    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você já é médico.')
        return redirect('/medicos/abrir_horario')

    if request.method ==  "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades': especialidades, 'is_medico': is_medico(request.user)})
    elif request.method == "POST":               
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        dados_medicos = DadosMedico(
           crm=crm,
           nome=nome,
           cep=cep,
           rua=rua,
           bairro=bairro,
           numero=numero,
           celuda_identidade_medica=cim,
           rg=rg,
           foto=foto,
           especialidade_id=especialidade,
           descricao=descricao,
           valor_consulta=valor_consulta,
           user=request.user
        )
       
        dados_medicos.save()
       
        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso.')
        return redirect('/medicos/abrir_horario')
    


def abrir_horario(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    
    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})
    
    elif request.method == "POST":
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')

        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A Data não pode ser menor que a data atual.')
            return redirect('/medicos/abrir_horario')
        
        horario_abrir = DatasAbertas(
            data=data,
            user=request.user,
        )
        
        horario_abrir.save()

        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso.')
        return redirect('/medicos/abrir_horario')
      


def consultas_medico(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    
    hoje = datetime.now().date()

    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id'))
    print(consultas_hoje.values)
    
    return render(request, 'consultas_medico.html', {'consultas_hoje' : consultas_hoje, 'consultas_restantes': consultas_restantes, 'is_medico': is_medico(request.user)})



def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair')
    

    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        return render(request, 'consulta_area_medico.html', {'consulta': consulta,'is_medico': is_medico(request.user)}) 
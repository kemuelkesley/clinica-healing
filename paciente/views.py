from django.shortcuts import render
from medico.models import DadosMedico

# Create your views here.

def home(request):
    if request.method == "GET":
        medicos = DadosMedico.objects.all()
        print(medicos)
        return render(request, 'home.html', {'medicos' : medicos})
    


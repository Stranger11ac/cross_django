from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')
    # return HttpResponse("<h1>Inicio Cross Project</h1>")

def faq(request):
    return render(request, 'faq.html')
    # return HttpResponse("<h1>Inicio Preguntas frecuentes</h1>")

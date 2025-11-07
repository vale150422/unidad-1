from django.shortcuts import render, redirect , get_object_or_404
from .models import Dibujo

def crear_dibujo(request):
    if request.method == 'POST':
        Autor = request.POST.get('Autor')
        tipo_Dibujo = request.POST.get('tipo_Dibujo')
        Valor = request.POST.get('Valor')
        fecha_Realizacion = request.POST.get('fecha_Realizacion')
        Dibujo = Dibujo(
            Autor=Autor,
            tipo_Dibujo=tipo_Dibujo,
            Valor=Valor,
            fecha_Realizacion=fecha_Realizacion
        )
        Dibujo.save()
        return redirect('lista_dibujo')
    return render(request, 'formulario_dibujo/crear_dibujo.html')




def lista_dibujo(request):
    Dibujo = Dibujo.objects.all()
    return render(request, 'formulario_motos/lista_dibujo.html', {'dibujo': Dibujo})



def eliminar_dibujo(request, dibujo_id):
    dibujo = get_object_or_404(Dibujo, id=dibujo_id)
    dibujo.delete()
    return redirect('lista_dibujo')
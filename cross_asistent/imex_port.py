from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse
from .models import Database, Mapa, Categorias
from .views import databaseall, mapaall
from django.utils import timezone
from .forms import CSVUploadForm
import csv

@login_required
@never_cache
def export_database(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M%S')
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="UTC_database_{now}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Categoria', 'Titulo', 'Informacion', 'Redirigir', 'Frecuencia', 'Documentos', 'Imagenes', 'Fecha Modificacion'])
        # Obtener todos los objetos del modelo Database
        
        for info in databaseall:
            writer.writerow([
                info.categoria if info.categoria else '',
                info.titulo,
                info.informacion,
                info.redirigir,
                info.frecuencia,
                info.documentos.url if info.documentos else '',
                info.imagenes.url if info.imagenes else '',
                info.fecha_modificacion
            ])
        return response

@login_required
@never_cache
def import_database(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            csv_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(csv_file)
            next(reader)  # Omitir la fila de encabezado
            for row in reader:
                categoria, _ = Categorias.objects.get_or_create(categoria=row[0])
                # Crear la instancia del modelo
                Database.objects.create(
                    categoria=categoria,
                    titulo=row[1],
                    informacion=row[2],
                    redirigir=row[3],
                    frecuencia=int(row[4]),
                    documentos=row[5],
                    imagenes=row[6],
                    fecha_modificacion=row[7]
                )
            # Redirigir a la vista programador después de procesar el formulario
        return JsonResponse({'success': True, 'message': 'Base de datos importada correctamente ✔'}, status=200)
    else:
        form = CSVUploadForm()
    

@login_required
@never_cache
def export_mapa(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M%S')
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="UTC_mapa_{now}.csv"'
        writer = csv.writer(response)
        writer.writerow(['nombre', 'informacion', 'color', 'door_cords', 'p1_polygons', 'p2_polygons', 'p3_polygons', 'p4_polygons'])
        
        for info in mapaall:
            writer.writerow([
                info.nombre,
                info.informacion,
                info.color,
                info.door_cords,
                info.p1_polygons,
                info.p2_polygons,
                info.p3_polygons,
                info.p4_polygons,
            ])
        return response

@login_required
@never_cache
def import_mapa(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            csv_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                # Crear la instancia del modelo
                Mapa.objects.create(
                    nombre=row[0],
                    informacion=row[1],
                    color=row[2],
                    door_cords=row[3],
                    p1_polygons=row[4],
                    p2_polygons=row[5],
                    p3_polygons=row[6],
                    p4_polygons=row[7]
                )
        return JsonResponse({'success': True, 'message': 'Mapa importado correctamente 🤘😋'}, status=200)
    else:
        form = CSVUploadForm()
    
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse
from .models import Database, Mapa, Categorias
from .views import databaseall, mapaall, categoriasall
from django.utils import timezone
from .forms import CSVUploadForm
import csv
import io

now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')

@login_required
@never_cache
def export_categorias(request):
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="UTC_categorias_{now}.csv"'
        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['ID', 'Categoria', 'Descripcion'])

        for item in categoriasall:
            writer.writerow([
                item.id,
                item.categoria if item.categoria else '',
                item.descripcion if item.descripcion else '',
            ])

        return response
    else:
        return JsonResponse({'error': True, 'message': 'Accion no permitida. 🧐😠🤥'}, status=400)

@login_required
@never_cache
def import_categorias(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                csv_file = io.TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(csv_file)
                next(reader)  # Omitir la fila de encabezado
                for row in reader:
                    Categorias.objects.create(
                        id=row[0],
                        categoria=row[1],
                        descripcion=row[2],
                    )
                return JsonResponse({'success': True, 'message': 'Categorías importadas correctamente. 🎉😁🫡'}, status=200)
            except UnicodeDecodeError:
                return JsonResponse({'success': False, 'message': 'Error de codificación. Asegúrese de que el archivo esté en formato UTF-8.'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error al importar categorías: {str(e)}'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Formulario no válido.'}, status=400)
    else:
        form = CSVUploadForm()
        return JsonResponse({'error': True, 'message': 'Método no permitido.'}, status=405)

@login_required
@never_cache
def export_database(request):
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="UTC_database_{now}.csv"'
        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['ID','Categoria', 'Titulo', 'Informacion', 'Redirigir', 'Frecuencia', 'Documentos', 'Imagenes', 'Evento:fecha de inicio', 'Evento:fecha de fin', 'Evento:lugar','Evento:className (CSS)', 'Fecha Modificacion'])
        
        for info in databaseall:
            writer.writerow([
                info.id,
                info.categoria if info.categoria else '',
                info.titulo if info.titulo else '',
                info.informacion if info.informacion else '',
                info.redirigir if info.redirigir else '',
                info.frecuencia if info.frecuencia else '',
                info.documento.url if info.documento else '',
                info.imagen.url if info.imagen else '',
                info.evento_fecha_inicio if info.evento_fecha_inicio else '',
                info.evento_fecha_fin if info.evento_fecha_fin else '',
                info.evento_lugar if info.evento_lugar else '',
                info.evento_className if info.evento_className else '',
                info.fecha_modificacion if info.fecha_modificacion else '',
            ])
        return response

@login_required
@never_cache
def import_database(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                csv_file = io.TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(csv_file)
                next(reader)  # Omitir la fila de encabezado
                for row in reader:
                    categoria, _ = Categorias.objects.get_or_create(categoria=row[1])
                    Database.objects.create(
                        id=row[0],
                        categoria=categoria,
                        titulo=row[2],
                        informacion=row[3],
                        redirigir=row[4],
                        frecuencia=int(row[5]),
                        documento=row[6],
                        imagen=row[7],
                        fecha_modificacion=row[8]
                    )
                return JsonResponse({'success': True, 'message': 'Base de Datos importadas correctamente. 🎉😁🫡'}, status=200)
            except UnicodeDecodeError:
                return JsonResponse({'success': False, 'message': 'Error de codificación. Asegúrese de que el archivo esté en formato UTF-8.'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error al importar Base de Datos: {str(e)}'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Formulario no válido.'}, status=400)
    else:
        form = CSVUploadForm()
        return JsonResponse({'error': True, 'message': 'Método no permitido.'}, status=405)

@login_required
@never_cache
def export_mapa(request):
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="UTC_mapa_{now}.csv"'
        response.write('\ufeff'.encode('utf8'))
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
            try:
                csv_file = io.TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(csv_file)
                next(reader)  # Omitir la fila de encabezado
                for row in reader:
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
                return JsonResponse({'success': True, 'message': 'Datos Del Mapa importados correctamente. 🎉😁🫡'}, status=200)
            except UnicodeDecodeError:
                return JsonResponse({'success': False, 'message': 'Error de codificación. Asegúrese de que el archivo esté en formato UTF-8.'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error al importar Datos Del Mapa: {str(e)}'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Formulario no válido.'}, status=400)
    else:
        form = CSVUploadForm()
        return JsonResponse({'error': True, 'message': 'Método no permitido.'}, status=405)
    
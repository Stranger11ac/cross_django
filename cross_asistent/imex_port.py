from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse
from .models import Database, Mapa, Categorias
from .views import databaseall, mapaall, categoriasall
from django.utils import timezone
from .forms import CSVUploadForm
import csv
import io

"""Crea una respuesta HTTP con contenido CSV."""
def create_csv_response(filename, header, rows):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write('\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    return response

@login_required
@never_cache
def export_categorias(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')
    if request.user.is_staff:
        rows = [
            [item.id, item.categoria if item.categoria else '', item.descripcion if item.descripcion else '']
            for item in categoriasall
        ]
        return create_csv_response(f"UTC_categorias_{now}.csv", ['ID', 'Categoria', 'Descripcion'], rows)
    return JsonResponse({'success': False, 'message': 'Acción no permitida. 🧐😠🤥'}, status=400)

@login_required
@never_cache
def import_categorias(request):
    return import_csv_data(request, Categorias, {
        'id': 0,
        'categoria': 1,
        'descripcion': 2,
    }, 'Categorías importadas correctamente. 🎉😁🫡')

@login_required
@never_cache
def export_database(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')
    if request.user.is_staff:
        rows = [
            [
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
            ]
            for info in databaseall
        ]
        return create_csv_response(f"UTC_database_{now}.csv", 
            ['ID', 'Categoria', 'Titulo', 'Informacion', 'Redirigir', 'Frecuencia', 'Documento', 'Imagen', 'Evento:fecha de inicio', 'Evento:fecha de fin', 'Evento:lugar', 'Evento:className (CSS)', 'Fecha Modificacion'], 
            rows
        )
    return JsonResponse({'success': False, 'message': 'Acción no permitida. 🧐😠🤥'}, status=400)

@login_required
@never_cache
def import_database(request):
    return import_csv_data(request, Database, {
        'id': 0,
        'categoria': lambda row: Categorias.objects.get_or_create(categoria=row[1])[0],
        'titulo': 2,
        'informacion': 3,
        'redirigir': 4,
        'frecuencia': lambda row: int(row[5]),
        'documento': 6,
        'imagen': 7,
        'fecha_modificacion': 8,
    }, 'Base de Datos importadas correctamente. 🎉😁🫡')

@login_required
@never_cache
def export_mapa(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')
    if request.user.is_staff:
        rows = [
            [
                info.nombre if info.nombre else '',
                info.informacion if info.informacion else '',
                info.color if info.color else '',
                info.door_cords if info.door_cords else '',
                info.p1_polygons if info.p1_polygons else '',
                info.p2_polygons if info.p2_polygons else '',
                info.p3_polygons if info.p3_polygons else '',
                info.p4_polygons if info.p4_polygons else '',
            ]
            for info in mapaall
        ]
        return create_csv_response(f"UTC_mapa_{now}.csv", 
            ['nombre', 'informacion', 'color', 'door_cords', 'p1_polygons', 'p2_polygons', 'p3_polygons', 'p4_polygons'], 
            rows
        )
    return JsonResponse({'success': False, 'message': 'Acción no permitida. 🧐😠🤥'}, status=400)

@login_required
@never_cache
def import_mapa(request):
    return import_csv_data(request, Mapa, {
        'nombre': 0,
        'informacion': 1,
        'color': 2,
        'door_cords': 3,
        'p1_polygons': 4,
        'p2_polygons': 5,
        'p3_polygons': 6,
        'p4_polygons': 7,
    }, 'Datos Del Mapa importados correctamente. 🎉😁🫡')

"""Importa datos desde un archivo CSV para un modelo específico."""
def import_csv_data(request, model, field_map, success_message):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                csv_file = io.TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(csv_file)
                next(reader)  # Omitir la fila de encabezado
                for row in reader:
                    data = {}
                    for field, index in field_map.items():
                        if callable(index):
                            data[field] = index(row)
                        else:
                            data[field] = row[index]
                    model.objects.create(**data)
                return JsonResponse({'success': True, 'message': success_message}, status=200)
            except UnicodeDecodeError:
                return JsonResponse({'success': False, 'message': 'Error de codificación. Asegúrese de que el archivo esté en formato UTF-8.'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error al importar datos: {str(e)}'}, status=400)
        return JsonResponse({'success': False, 'message': 'Formulario no válido.'}, status=400)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

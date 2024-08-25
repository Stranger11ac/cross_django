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


"""Convierte el valor en un booleano. Devuelve False si no es "True"."""
def parse_all_day(value):
    return value.strip().lower() == 'true'

@login_required
@never_cache
def export_categorias(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')
    if request.user.is_staff:
        rows = [
            [item.categoria or '', item.descripcion or '']
            for item in categoriasall
        ]
        return create_csv_response(f"UTC_categorias_{now}.csv", ['Categoria', 'Descripcion'], rows)
    return JsonResponse({'success': False, 'message': 'Acción no permitida. 🧐😠🤥'}, status=400)

@login_required
@never_cache
def import_categorias(request):
    return import_csv_data(request, Categorias, {
        'categoria': 0,
        'descripcion': 1,
    }, 'Categorías importadas correctamente. 🎉😁🫡')

@login_required
@never_cache
def export_database(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')
    if request.user.is_staff:
        rows = [
            [
                info.categoria or '',
                info.titulo or '',
                info.informacion or '',
                info.redirigir or '',
                info.frecuencia,
                info.uuid or '',
                info.evento_fecha_inicio or '',
                info.evento_fecha_fin or '',
                info.evento_allDay,
                info.evento_lugar or '',
                info.evento_className or '',
                info.fecha_modificacion or '',
            ]
            for info in databaseall
        ]
        return create_csv_response(f"UTC_database_{now}.csv", 
            ['Categoria', 'Titulo', 'Informacion', 'Redirigir', 'Frecuencia', 'uuid','Evento:fecha de inicio', 'Evento:fecha de fin', 'Evento:Todo el dia','Evento:lugar', 'Evento:className (CSS)', 'Fecha Modificacion'], 
            rows
        )
    return JsonResponse({'success': False, 'message': 'Acción no permitida. 🧐😠🤥'}, status=400)

@login_required
@never_cache
def import_database(request):
    return import_csv_data(request, Database, {
        'categoria': lambda row: Categorias.objects.get_or_create(categoria=row[0])[0],
        'titulo': 1,
        'informacion': 2,
        'redirigir': 3,
        'frecuencia': lambda row: int(row[4]),
        'uuid': 5,
        'evento_fecha_inicio': 6,
        'evento_fecha_fin': 7,
        'evento_allDay': lambda row: parse_all_day(row[8]),
        'evento_lugar': 9,
        'evento_className': 10,
        'fecha_modificacion': 11,
    }, 'Base de Datos importadas correctamente. 🎉😁🫡')

@login_required
@never_cache
def export_mapa(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')
    if request.user.is_staff:
        rows = [
            [
                info.uuid or '',
                info.nombre or '',
                info.informacion or '',
                info.color or '',
                info.door_cords or '',
                info.p1_polygons or '',
                info.p2_polygons or '',
                info.p3_polygons or '',
                info.p4_polygons or '',
            ]
            for info in mapaall
        ]
        return create_csv_response(f"UTC_mapa_{now}.csv", 
            ['uuid', 'Nombre', 'Informacion', 'Color', 'Coordenadas: Puerta', 'Coordenadas: Esquina 1', 'Coordenadas: Esquina 2', 'Coordenadas: Esquina 3', 'Coordenadas: Esquina 4'], 
            rows
        )
    return JsonResponse({'success': False, 'message': 'Acción no permitida. 🧐😠🤥'}, status=400)

@login_required
@never_cache
def import_mapa(request):
    return import_csv_data(request, Mapa, {
        'uuid': 0,
        'nombre': 1,
        'informacion': 2,
        'color': 3,
        'door_cords': 4,
        'p1_polygons': 5,
        'p2_polygons': 6,
        'p3_polygons': 7,
        'p4_polygons': 8,
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
                return JsonResponse({'success': True, 'functions':'reload', 'message': success_message}, status=200)
            except UnicodeDecodeError:
                return JsonResponse({'success': False, 'message': 'Error de codificación. Asegúrese de que el archivo esté en formato UTF-8.'}, status=400)
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error al importar datos: {str(e)}'}, status=400)
        return JsonResponse({'success': False, 'message': 'Formulario no válido.'}, status=400)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

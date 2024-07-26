from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.views.decorators.cache import never_cache
from .forms import BannersForm
from django.contrib.auth.models import User
from django.db import models, transaction
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from . import functions, models
import json

databaseall = models.Database.objects.all()
mapaall = models.Mapa.objects.all()
categoriasall = models.Categorias.objects.all()

def index(request):
    if not request.user.is_staff:
        logout(request)
    banners_all = models.Banners.objects.filter(visible=True)
    banners_modificados = []

    for banner in banners_all:
        imagen_url = banner.imagen.url.replace("/cross_asistent", "")
        banners_modificados.append({
            'id': banner.id,
            'titulo': banner.titulo,
            'descripcion': banner.descripcion,
            'articulo': banner.articulo,
            'imagen': imagen_url,
        })

    return render(request, 'index.html', {
        'banners': banners_modificados,
        'active_page': 'inicio'
    })

def faq(request):
    if not request.user.is_staff:
        logout(request)
    questall = models.Database.objects.filter(frecuencia__gt=0).order_by('-frecuencia')
    return render(request, 'frecuentes.html', {
        'quest_all': questall,
        'active_page': 'faq'
    })

def crear_pregunta(request):    
    if request.method == "POST":
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                preguntaPOST = data['pregunta']
                descripcionPOST = data['descripcion']
                categoria_preguntas = models.Categorias.objects.get(id=1) 

                pregunta = models.Preguntas(pregunta=preguntaPOST, descripcion=descripcionPOST)
                pregunta.save()
                
                models.Notificacion.objects.create(
                    usuario=request.user,
                    tipo='Pregunta',
                    mensaje=f'{request.user.username} ha realizado una nueva pregunta: "{preguntaPOST}".',
                )

                return JsonResponse({'success': True, 'message': 'Gracias por tu pregunta ❤️💕😁👍 '}, status=200)
            except Exception as e:
                print(f'Hay un error en: {e}')
                return JsonResponse({'success': False, 'message': 'Ups! 😥😯 hubo un error y tu pregunta no se pudo registrar. Por favor intente de nuevo más tarde.'}, status=400)
        else:
            print('error, no JSON')
            return JsonResponse({'success': False, 'message': 'Error: no se permite este tipo de archivo '}, status=400)
    return render(request, 'frecuentes.html', {'quest_all': models.Preguntas.objects.all()})

def blogs(request):
    if not request.user.is_staff:
        logout(request)
    blogs = models.Articulos.objects.all()
    blogs_modificados = []

    for oneblog in blogs:
        imagen_url = oneblog.encabezado
        if not imagen_url == '':
            img = oneblog.encabezado.url.replace("/cross_asistent", "")
            imgClass = 'item_img-url'
        else:
            img = '/static/img/default_image.webp'
            imgClass = 'item_title-full'

        blogs_modificados.append({
            'id': oneblog.id,
            'titulo': oneblog.titulo,
            'autor': oneblog.autor,
            'imagen': img,
            'class': imgClass,
        })
    return render(request, 'blogs.html', {
        'blogs_all': blogs_modificados,
        'active_page': 'blog'
    })

def mostrar_blog(request, Articulos_id):
    if not request.user.is_staff:
        logout(request)
    Articulos = models.Articulos.objects.filter(pk=Articulos_id)
    return render(request, 'mostrar_blogs.html', {'Articulos': Articulos})

def calendario(request):
    if not request.user.is_staff:
        logout(request)
    return render(request, 'calendario.html', {
        'active_page': 'calendario'
    })

def map(request):
    if not request.user.is_staff:
        logout(request)
    return render(request, 'mapa.html', {
        'active_page': 'map'
    })

def about(request):
    if not request.user.is_staff:
        logout(request)
    return render(request, 'about.html', {
        'active_page': 'about'
    })

# Administracion ----------------------------------------------------------
@never_cache
def singup(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        response = functions.create_newuser(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password1=request.POST.get('password1'),
            password2=request.POST.get('password2'),
        )
        if response['success']:
            user = User.objects.get(username=request.POST.get('username'))
            models.Notificacion.objects.create(
                usuario=user,
                tipo='Registro',
                mensaje=f'{user.username} se ha registrado y necesita activación.',
            )
        response['functions'] = 'reload'
        status = 200 if response['success'] else 400
        return JsonResponse(response, status=status)
    else:
        logout(request)
        return redirect('singin')

@never_cache
def singinpage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        login_identifier = request.POST.get('username')  # Puede ser username o email
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=login_identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=login_identifier)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            if not user.is_active:
                return JsonResponse({'success': False, 'functions': 'singin', 'message': '🧐😥😯 UPS! <br> Al parecer tu cuenta esta <u>Inactiva</u>. Tu cuenta será activada si estas autorizado'}, status=400)
            
            user = authenticate(request, username=user.username, password=password)
            if user is None:
                return JsonResponse({'success': False, 'functions': 'singin', 'message': 'Revisa el usuario o contraseña 😅.'}, status=400)
            else:
                login(request, user)
                pageRedirect = reverse('vista_admin')
                if user.is_staff:
                    pageRedirect = reverse('vista_programador')
                return JsonResponse({'success': True, 'functions': 'singin', 'redirect_url': pageRedirect}, status=200)
        else:
            return JsonResponse({'success': False, 'functions': 'singin', 'message': 'Usuario no registrado 😅. Verifica tu nombre de usuario o correo electrónico'}, status=400)
    else:
        logout(request)
        return render(request, 'singinup.html', {
            'active_page': 'singin'
        })

@login_required
@never_cache
def singout(request):
    logout(request)
    return redirect('singin')

# Perfiles ----------------------------------------------------------
@login_required
@never_cache
def vista_admin(request):
    blogs_all = models.Articulos.objects.filter()
    user = request.user
    context = {
        'user': user,
        'num_blogs': blogs_all.count(),
        'blogs_all': blogs_all,
        'active_page': 'home',
        'pages': functions.pages
    }
    return render(request, 'admin/vista_admin.html', context)

@login_required
@never_cache
def vista_programador(request):
    blogs_all = models.Articulos.objects.all()
    banners_all = models.Banners.objects.all()
    users = User.objects.all().order_by('-id')
    contexto = {
        'user': request.user,
        'users': users,
        'total_usuarios': users.count(),
        'banners_all': banners_all,
        'total_banners': banners_all.count(),
        'num_blogs': blogs_all.count(),
        'num_preguntas': databaseall.count(),
        'active_page': 'home',
        'categorias': categoriasall,
        'pages': functions.pages
    }
    
    if request.method == 'POST':
        response = functions.create_newuser(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password1=request.POST.get('password'),
            is_staff=request.POST.get('is_staff', False),
            is_active=request.POST.get('is_active', False),
        )
        response['position'] = 'top'
        response['functions'] = 'reload'
        status = 200 if response['success'] else 400
        return JsonResponse(response, status=status)

    return render(request, 'admin/vista_programador.html', contexto)

@login_required
@never_cache
def ver_perfil(request):
    perfil_usuario = request.user
    return render(request, 'admin/perfil.html', {'perfil_usuario': perfil_usuario, 'active_page': 'perfil', 'pages': functions.pages})

@login_required
@never_cache
def ver_notis(request):
    notificaciones = models.Notificacion.objects.all().order_by('-fecha')
    return render(request, 'admin/notificaciones.html', {'notificaciones': notificaciones, 'pages': functions.pages})

def marcar_notificaciones_leidas(request):
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        models.Notificacion.objects.filter(id__in=ids).update(leida=True)
        # return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'success', 'message': f'Notificcacion {ids}, se marco como leida para todos los usuarios', 'icon': 'info'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ocurrio un error😯😥 <br>{str(e)}', 'icon': 'error'}, status=400)

# Banners ----------------------------------------------------------
@login_required
@never_cache
def upload_banner(request):
    if request.method == 'POST':
        form = BannersForm(request.POST, request.FILES)
        if form.is_valid():
            banner = form.save(commit=False)  
            if not request.FILES.get('imagen'):  
                banner.imagen = 'static/img/default_image.webp'  # Asegúrate de que esta ruta sea correcta y la imagen exista
            banner.save()  

            models.Notificacion.objects.create(
                usuario=request.user,
                tipo='Banner',
                mensaje=f'{request.user.username} ha subido un nuevo banner titulado "{banner.titulo}".',
            )
            return redirect('upload_banner')
    else:
        form = BannersForm()
    
    banners_all = models.Banners.objects.all()
    banners_modificados = []

    for banner in banners_all:
        imagen_url = banner.imagen.url.replace("/cross_asistent", "")
        banners_modificados.append({
            'id': banner.id,
            'titulo': banner.titulo,
            'descripcion': banner.descripcion,
            'articulo': banner.articulo,
            'imagen': imagen_url,
            'expiracion': banner.expiracion,
        })
    context = { 'banners': banners_modificados, 'active_page': 'banner','pages': functions.pages }
    return render(request, 'admin/banners.html', context)

@login_required
@never_cache
def edit_banner(request, banner_id):
    banner = get_object_or_404(models.Banners, id=banner_id)
    if request.method == 'POST':
        # Obtener la nueva imagen del formulario si se proporciona
        new_image = request.FILES.get('imagen')
        
        # Guardar la nueva imagen si se proporciona
        if new_image:
            # Eliminar la imagen anterior si existe
            if banner.imagen:
                if default_storage.exists(banner.imagen.name):
                    default_storage.delete(banner.imagen.name)
            
            # Guardar la nueva imagen en el modelo
            banner.imagen = new_image
        
        # Actualizar otros campos del banner si es necesario
        banner.titulo = request.POST.get('titulo')
        banner.descripcion = request.POST.get('descripcion')
        banner.articulo = request.POST.get('articulo')
        banner.expiracion = request.POST.get('expiracion')
        
        # Guardar el banner actualizado
        banner.save()
        
        return JsonResponse({
            'success': True,
            'functions': 'reload',
            'message': f'El banner <u>{banner.titulo}</u> fue modificado exitosamente 🥳🎉🎈.'
        }, status=200)
    
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

@login_required
@never_cache
def delete_banner(request, banner_id):
    if request.method == 'POST':
        icon = 'warning'
        banner = get_object_or_404(models.Banners, id=banner_id)
        banner.delete()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': 'Banner eliminado exitosamente.', 'icon': icon}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

# Base de Datos ----------------------------------------------------------
@login_required
@never_cache
def database_page(request):
    datos_modificados = []

    for dato in databaseall:        
        if dato.imagenes:
            imagen_url = dato.imagenes.url.replace("/cross_asistent", "")
        else:
            imagen_url = ''
        if dato.documentos:
            documento_url = dato.documentos.url.replace("/cross_asistent", "")
        else:
            documento_url = ''
        datos_modificados.append({
            'categoria': dato.categoria,
            'titulo': dato.titulo,
            'informacion': dato.informacion,
            'redirigir': dato.redirigir,
            'frecuencia': dato.frecuencia,
            'documento': documento_url,
            'imagen': imagen_url,
            'modificacion': dato.fecha_modificacion,
        })
    context = { 'database': datos_modificados, 'active_page': 'database','pages': functions.pages, 'categorias': categoriasall }
    return render(request, 'admin/database.html', context)
    
# Blogs ----------------------------------------------------------
@login_required
@never_cache
def create_blog(request):
    if request.method == 'POST':
        try:
            tituloPOST = request.POST.get('titulo')
            autorPOST = request.POST.get('autor')
            contenidoPOST = request.POST.get('contenidoWord')
            encabezadoPOST = request.FILES.get('encabezadoImg')

            articulo = models.Articulos(
                titulo=tituloPOST,
                contenido=contenidoPOST,
                autor=autorPOST,
                encabezado=encabezadoPOST
            )
            articulo.save()
            models.Notificacion.objects.create(
                usuario=request.user,
                tipo='Blog',
                mensaje=f'{request.user.username} ha subido un nuevo blog titulado "{articulo.titulo}".',
            )

            return JsonResponse({'success': True, 'message': 'Excelente 🥳🎈🎉. Tu articulo ya fue publicado. Puedes editarlo cuando gustes. 🧐😊'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ocurrio un error😯😥 <br>{str(e)}'}, status=400)
    return render(request, 'admin/blog.html', {'active_page': 'blog','pages': functions.pages})

@login_required
@never_cache
def upload_image(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES['file']
            imagen_articulo = models.ImagenArticulo(imagen=image_file)
            imagen_articulo.save()
            image_url = imagen_articulo.imagen.url.replace("/cross_asistent", "")

            return JsonResponse({'location': image_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Error al subir la imagen'}, status=400)

@login_required
@never_cache
def lista_imagenes(request):
    imagenes = models.ImagenArticulo.objects.all()
    imagenes_modificadas = []

    for imagen in imagenes:
        imagen_url = imagen.imagen.url.replace("/cross_asistent", "")
        imagenes_modificadas.append({
            'id': imagen.id,
            'url': imagen_url
        })
    return render(request, 'admin/blog_imgs.html', {'imagenes': imagenes_modificadas})

#Mapa ----------------------------------------------------------
@login_required
@never_cache
def update_mapa(request):
    categoria_mapa = models.Categorias.objects.get(categoria="Mapa")
    map_inDB = models.Database.objects.filter(categoria=categoria_mapa)
    return render(request, 'admin/mapa.html', {'map_inDB': map_inDB, 'active_page': 'mapa','pages': functions.pages})

@login_required
@never_cache
def obtenerEdificio(request):
    if request.method == 'GET':
        edificio_id = request.GET.get('id')
        if (edificio_id):
            edificio = get_object_or_404(models.Database, id=edificio_id)
            data = {
                'titulo': edificio.titulo,
                'informacion': edificio.informacion,
                'imagen_url': edificio.imagenes.url if edificio.imagenes else None,
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@never_cache
def regEdificioMapa(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Metodo no valido'}, status=400)

    isNewPost = request.POST.get('isNew')
    nombrePost = request.POST.get('titulo')
    colorPost = request.POST.get('color')
    p1Post = request.POST.get('p1_polygons')
    p2Post = request.POST.get('p2_polygons')
    p3Post = request.POST.get('p3_polygons')
    p4Post = request.POST.get('p4_polygons')
    informacionText = request.POST.get('textTiny')
    informacionPost = request.POST.get('contenidoWord')
    door_cordsPost = request.POST.get('door_cords')
    imagenPost = request.FILES.get('imagenes')

    with transaction.atomic():
        if isNewPost is None:
            # Update existing Mapa
            if models.Mapa.objects.filter(nombre=nombrePost).exists():
                edificio = get_object_or_404(models.Mapa, nombre=nombrePost)
                edificio.color = colorPost
                edificio.p1_polygons = p1Post
                edificio.p2_polygons = p2Post
                edificio.p3_polygons = p3Post
                edificio.p4_polygons = p4Post
                edificio.door_cords = door_cordsPost
                edificio.informacion = informacionPost
                edificio.save()
                success_message = f'Se Actualizo el "{nombrePost}", los cambios se reflejaran en el mapa 🧐😊🎈'
            else:
                models.Mapa.objects.create(
                    nombre=nombrePost,
                    color=colorPost,
                    p1_polygons=p1Post,
                    p2_polygons=p2Post,
                    p3_polygons=p3Post,
                    p4_polygons=p4Post,
                    door_cords=door_cordsPost,
                    informacion=informacionPost,
                )
                success_message = f'El "{nombrePost}" se creo exitosamente en el Mapa 🎉🎈🥳'

            if imagenPost:
                mapIndb = get_object_or_404(models.Database, nombre=nombrePost)
                mapIndb.imagenes = imagenPost
                mapIndb.save()
            return JsonResponse({'success': True, 'message': success_message}, status=200)

        # Create new Mapa and Database
        models.Mapa.objects.create(
            nombre=nombrePost,
            color=colorPost,
            p1_polygons=p1Post,
            p2_polygons=p2Post,
            p3_polygons=p3Post,
            p4_polygons=p4Post,
            door_cords=door_cordsPost,
            informacion=informacionPost,
        )
        
        models.Database.objects.create(
            categoria=models.Categorias.objects.get(categoria="Mapa"),
            nombre=nombrePost,
            informacion=informacionText,
            imagenes=imagenPost
        )

        return JsonResponse({'success': True, 'message': 'Se creo un nuevo edificio en el mapa y en la base de datos de forma exitosa 🎉🎉🎉'}, status=200)

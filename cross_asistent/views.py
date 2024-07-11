from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.core.files.storage import default_storage
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from .forms import BannersForm, ProfileImageForm
from django.contrib.auth.models import User
from django.db import models, transaction
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.apps import apps
from . import functions, models
import json
from django.contrib.auth.decorators import permission_required

databaseall = models.Database.objects.all()
mapaall = models.Mapa.objects.all()

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
                tituloPOST = data['pregunta']
                categoria_preguntas = models.Categorias.objects.get(id=1) 

                pregunta = models.Database(titulo=tituloPOST, categoria=categoria_preguntas)
                pregunta.save()
                models.Notificacion.objects.create(
                    usuario=request.user,
                    tipo='Pregunta',
                    mensaje=f'El usuario {request.user.username} ha realizado una nueva pregunta: "{tituloPOST}".',
                )

                return JsonResponse({'success': True, 'message': 'Gracias por tu pregunta ❤️💕😁👍 '}, status=200)
            except Exception as e:
                print(f'Hay un error en: {e}')
                return JsonResponse({'success': False, 'message': 'Ups! 😥😯 hubo un error y tu pregunta no se pudo registrar. por favor intente de nuevo mas tarde.'}, status=400)
        else:
            print('error, no JSON')
            return JsonResponse({'success': False, 'message': 'Error: no se permite este tipo de archivo '}, status=400)
    return render(request, 'frecuentes.html', {'quest_all': databaseall})

def blogs(request):
    if not request.user.is_staff:
        logout(request)
    blogs = models.Articulos.objects.all()
    blogs_modificados = []

    for oneblog in blogs:
        imagen_url = oneblog.encabezado
        if not imagen_url == '':
            img = oneblog.encabezado.url.replace("/cross_asistent", "")
        else:
            img = ''
        blogs_modificados.append({
            'id': oneblog.id,
            'titulo': oneblog.titulo,
            'autor': oneblog.autor,
            'imagen': img,
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
def singuppage(request):
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
                mensaje=f'El usuario {user.username} se ha registrado y necesita activación.',
            )
        response['functions'] = 'reload'
        status = 200 if response['success'] else 400
        return JsonResponse(response, status=status)
    else:
        logout(request)
        return render(request, 'singin')

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
        return render(request, 'admin/singin.html', {
            'active_page': 'singin'
        })

@login_required
@never_cache
def singoutpage(request):
    logout(request)
    return redirect('singin')

# def para la vista administrador
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
    categorias_all = models.Categorias.objects.all()
    users = User.objects.all()
    contexto = {
        'user': request.user,
        'users': users,
        'total_usuarios': users.count(),
        'banners_all': banners_all,
        'total_banners': banners_all.count(),
        'num_blogs': blogs_all.count(),
        'num_preguntas': databaseall.count(),
        'active_page': 'home',
        'categorias': categorias_all,
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
        response['functions'] = 'reload'
        status = 200 if response['success'] else 400
        return JsonResponse(response, status=status)

    return render(request, 'admin/vista_programador.html', contexto)

# crear  blog --------------------------------------
@login_required
def crear_articulo(request):
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
                mensaje=f'El usuario {request.user.username} ha subido un nuevo blog titulado "{articulo.titulo}".',
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


#Consulta para informacion del Mapa --------------------------------
@login_required
def obtenerinfoEdif(request):
    categoria_mapa = models.Categorias.objects.get(categoria="Mapa")
    map_inDB = models.Database.objects.filter(categoria=categoria_mapa)
    return render(request, 'admin/mapa.html', {'map_inDB': map_inDB, 'active_page': 'mapa','pages': functions.pages})

@login_required
def obtenerEdificio(request):
    if request.method == 'GET':
        edificio_id = request.GET.get('id')
        if (edificio_id):
            edificio = get_object_or_404(models.Database, id=edificio_id)
            data = {
                'titulo': edificio.nombre,
                'informacion': edificio.informacion,
                'imagen_url': edificio.imagenes.url if edificio.imagenes else None,
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
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


# subir banners ----------------------------------------------
@login_required
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
                mensaje=f'El usuario {request.user.username} ha subido un nuevo banner titulado "{banner.titulo}".',
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
def delete_banner(request, banner_id):
    if request.method == 'POST':
        icon = 'warning'
        banner = get_object_or_404(models.Banners, id=banner_id)
        banner.delete()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': 'Banner eliminado exitosamente.', 'icon': icon}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

@login_required
@never_cache
def ver_perfil(request):
    perfil_usuario = request.user

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        else:
            print(form.errors)  # Añade esto para ver errores en el formulario
    else:
        form = ProfileImageForm(instance=perfil_usuario)

    return render(request, 'admin/perfil.html', {'perfil_usuario': perfil_usuario, 'form': form, 'active_page': 'perfil', 'pages': functions.pages})

def password_reset_request(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        email = request.POST.get('email')
        print(f"Email recibido: {email}")

        if email:
            try:
                user = User.objects.get(email=email)
                print(f"Usuario encontrado: {user}")

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

                subject = "Reestablecer la contraseña"
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                print(f"Enlace de restablecimiento: {reset_link}")

                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                print("Correo enviado exitosamente")

                return JsonResponse({'success': True, 'message': 'Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.'}, status=200)
            except User.DoesNotExist:
                print("Usuario no encontrado")
                return JsonResponse({'success': False, 'message': 'El correo electrónico no está registrado.'}, status=400)
        else:
            print("No se proporcionó correo electrónico")
            return JsonResponse({'success': False, 'message': 'Por favor, ingresa tu correo electrónico.'}, status=400)
    else:
        return render(request, 'reset_pass.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                login(request, user)
                return redirect('password_reset_complete')
            else:
                return render(request, 'password_reset_confirm.html', {'validlink': True, 'error': 'Las contraseñas no coinciden.'})
        else:
            return render(request, 'password_reset_confirm.html', {'validlink': True})
    else:
        return render(request, 'password_reset_confirm.html', {'validlink': False})

@login_required
def ver_notis(request):
    notificaciones = models.Notificacion.objects.all().order_by('-fecha')
    return render(request, 'admin/notificaciones.html', {'notificaciones': notificaciones, 'pages': functions.pages})
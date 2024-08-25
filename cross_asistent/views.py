from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.db import models, transaction
from django.http import JsonResponse
from django.urls import reverse
from . import functions, models
import json

mapaall = models.Mapa.objects.all()
databaseall = models.Database.objects.all()
categoriasall = models.Categorias.objects.all()
questions_all = models.Preguntas.objects.all().order_by('-id')
categoriasFilter = models.Categorias.objects.exclude(categoria__in=['Mapa', 'Calendario'])

def index(request):
    if not request.user.is_staff:
        logout(request)
    banners_all = models.Banners.objects.filter(visible=True)
    banners_modificados = []

    for banner in banners_all:
        # imagen_url = banner.imagen.url.replace("cross_asistent/", "")
        imagen_url = banner.imagen.url
        banners_modificados.append({
            'id': banner.id,
            'titulo': banner.titulo,
            'descripcion': banner.descripcion,
            'redirigir': banner.redirigir,
            'imagen': imagen_url,
            'onlyImg': banner.solo_imagen,
        })

    return render(request, 'index.html', {
        'banners': banners_modificados,
        'active_page': 'inicio'
    })

def fqt_questions(request):
    if not request.user.is_staff:
        logout(request)
    
    categoria_Preguntas = models.Categorias.objects.get(categoria="Preguntas")
    questall = models.Database.objects.filter(frecuencia__gt=0, categoria=categoria_Preguntas).order_by('-frecuencia')
    return render(request, 'frecuentes.html', {
        'quest_all': questall,
        'active_page': 'faq'
    })

def fqt_questions_send(request):    
    if request.method == "POST":
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                preguntaPOST = data['pregunta']
                descripcionPOST = data['descripcion']

                pregunta = models.Preguntas(pregunta=preguntaPOST, descripcion=descripcionPOST)
                pregunta.save()

                return JsonResponse({'success': True, 'message': 'Gracias por tu pregunta. ❤️💕😁👍 <br>La responderemos lo mas pronto posible. 😁😊🫡'}, status=200)
            except Exception as e:
                print(f'Hay un error en: {e}')
                return JsonResponse({'error':True, 'success': False, 'message': 'Ups! 😥😯 hubo un error y tu pregunta no se pudo registrar. Por favor intente de nuevo más tarde.'}, status=400)
        else:
            print('error, no JSON')
            return JsonResponse({'error':True, 'success': False, 'message': 'Error: no se permite este tipo de archivo '}, status=400)
    return render(request, 'frecuentes.html', {'quest_all': models.Preguntas.objects.all()})

def blogs(request):
    if not request.user.is_staff:
        logout(request)
    blogs = models.Articulos.objects.all().order_by('-id')
    blogs_modificados = []

    for oneblog in blogs:
        imagen_url = oneblog.encabezado
        if not imagen_url == '':
            img = oneblog.encabezado.url
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
    return render(request, 'blogs_all.html', {
        'blogs_all': blogs_modificados,
        'active_page': 'blog'
    })

def mostrar_blog(request, Articulos_id):
    if not request.user.is_staff:
        logout(request)
    
    articulo = get_object_or_404(models.Articulos, pk=Articulos_id)
    autor_username = articulo.autor
    if articulo.encabezado:
        encabezado_url = articulo.encabezado.url
    else:
        encabezado_url = ''
    
    try:
        user_profile = models.UserProfile.objects.get(user__username=autor_username)
        user = User.objects.get(username=autor_username)
        if user_profile.blog_firma:
            firma_autor = user_profile.blog_firma
        else:
            firma_autor = f'{user.first_name} {user.last_name}'
    except models.UserProfile.DoesNotExist:
        firma_autor = autor_username
    except User.DoesNotExist:
        firma_autor = autor_username

    return render(request, 'blog.html', {
        'articulo': articulo,
        'firma_autor': firma_autor,
        'encabezado_url': encabezado_url,
    })

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
    banners_all = models.Banners.objects.all()
    users = User.objects.all().order_by('-id')
    contexto = {
        'users':users,
        'user':request.user,
        'active_page':'home',
        'pages':functions.pages,
        'categorias':categoriasFilter,
        'banners_all':banners_all,
        'preguntas_sending':questions_all,
        'num_preguntas':databaseall.count(),
        'num_blogs':models.Articulos.objects.filter(autor=request.user).count(),
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
    perfil_extencion = request.user.userprofile
    if perfil_extencion.profile_picture:
        request.user.userprofile.profile_picture = request.user.userprofile.profile_picture.url
    else:
        request.user.userprofile.profile_picture = '/static/img/UTC_logo-plano.webp'
    
    if not perfil_extencion.blog_firma:
        perfil_extencion.blog_firma = ''
                
    return render(request, 'admin/perfil.html', {
        'user_profile': perfil_extencion,
        'active_page': 'perfil',
        'pages': functions.pages
    })

@login_required
@never_cache
def ver_notis(request):
    notificaciones = models.Notificacion.objects.all().order_by('-fecha')
    return render(request, 'admin/notificaciones.html', {'notificaciones': notificaciones, 'pages': functions.pages})

@login_required
@never_cache
def marcar_notificaciones_leidas(request):
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        models.Notificacion.objects.filter(id__in=ids).update(leida=True)
        # return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'success', 'message': f'Notificacion {ids}, se marco como leida para todos los usuarios', 'icon': 'info'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ocurrió un error😯😥 <br>{str(e)}', 'icon': 'error'}, status=400)

# Banners ----------------------------------------------------------
@login_required
@never_cache
def banners_page(request):
    if request.method == 'POST':
        soloImagenPOST = request.POST.get('soloImagen')
        if soloImagenPOST == None:
            soloImagenPOST = False
        expiracionPOST = request.POST.get('expiracion')
        if expiracionPOST:
            expiracionPOST = expiracionPOST
        else:
            expiracionPOST = None
            
        banner = models.Banners(
            titulo = request.POST.get('contenidoWord'),
            descripcion = request.POST.get('descripcion'),
            redirigir = request.POST.get('redirigir'),
            imagen = request.FILES.get('imagen'),
            solo_imagen = soloImagenPOST,
            expiracion = expiracionPOST
        )
        banner.save()
        
        return JsonResponse({
            'success': True,
            'functions': 'reload',
            'message': f'Se realizo un post🎈.'
            # 'message': f'El banner {banner.titulo} fue creado exitosamente 🥳🎉🎈.'
        }, status=200)
    
    banners_all = models.Banners.objects.all()
    banners_modificados = []

    for banner in banners_all:
        banners_modificados.append({
            'id': banner.id,
            'titulo': banner.titulo,
            'descripcion': banner.descripcion,
            'redirigir': banner.redirigir,
            'imagen': banner.imagen.url,
            'expiracion': banner.expiracion if not banner.expiracion == None else '',
            'visible': banner.visible,
            'onlyImg': banner.solo_imagen,
        })
    context = { 'banners': banners_modificados,
               'active_page': 'banner',
               'pages': functions.pages,
               'banners_cound': banners_all.count() }
    return render(request, 'admin/banners.html', context)

# Base de Datos ----------------------------------------------------------
@login_required
@never_cache
def database_page(request):
    datos_modificados = []
    # for dato in databaseall.order_by('-id'):
    #     if dato.imagen:
    #         imagen_url = dato.imagen.url
    #     else:
    #         imagen_url = ''
    #     if dato.documento:
    #         documento_url = dato.documento.url
    #     else:
    #         documento_url = ''
    #     datos_modificados.append({
    #         'id': dato.id,
    #         'categoria': dato.categoria,
    #         'titulo': dato.titulo,
    #         'informacion': dato.informacion,
    #         'redirigir': dato.redirigir,
    #         'frecuencia': dato.frecuencia,
    #         'documento': documento_url,
    #         'imagen': imagen_url,
    #         'fecha_modificacion': dato.fecha_modificacion,
    #     })
    context = { 'active_page':'database','pages':functions.pages, 'preguntas_sending':questions_all, 'categorias':categoriasFilter, 'categoriasall':categoriasall, 'database': datos_modificados }
    return render(request, 'admin/database.html', context)

@login_required
@never_cache
def calendario_page(request):
    context = { 'active_page': 'calendario', 'pages': functions.pages }
    return render(request, 'admin/calendario.html', context)
    
# Blogs ----------------------------------------------------------
@login_required
@never_cache
def blog_page(request):
    if request.method == 'POST':
        try:
            autorPOST = request.POST.get('autor')
            tituloPOST = request.POST.get('titulo')
            contenidoWordPOST = request.POST.get('contenidoWord')
            encabezadoImgPOST = request.FILES.get('encabezadoImg')
            blogUpdate = request.POST.get('blogNewUpdate')
            
            if not blogUpdate == None and not blogUpdate == 'newBlog':
                blogUpdate = get_object_or_404(models.Articulos, id=blogUpdate)
                blogUpdate.autor = autorPOST
                blogUpdate.titulo = tituloPOST
                blogUpdate.contenido = contenidoWordPOST
                if encabezadoImgPOST:
                    blogUpdate.encabezado = encabezadoImgPOST
                blogUpdate.save()
                jsonMessage='Excelente 🥳🎈🎉. Tu articulo fue <span>modificado</span> de forma exitosa. 😁🫡'
                
                models.Notificacion.objects.create(
                    usuario=request.user,
                    tipo='Blog',
                    mensaje=f'{request.user.username} ha Modificado su blog titulado "{tituloPOST}".',
                )
                
            else:
                articulo = models.Articulos(
                    autor=autorPOST,
                    titulo=tituloPOST,
                    contenido=contenidoWordPOST,
                    encabezado=encabezadoImgPOST,
                )
                articulo.save()
                jsonMessage='Excelente 🥳🎈🎉. Tu artículo ya fue publicado. Puedes editarlo cuando gustes. 🧐😊'
                
                models.Notificacion.objects.create(
                    usuario=request.user,
                    tipo='Blog',
                    mensaje=f'{request.user.username} ha subido un nuevo blog titulado "{articulo.titulo}".',
                )
                
            user_perfil = request.user.userprofile
            if request.POST.get('new_firma'):
                user_perfil.blog_firma = request.POST.get('new_firma')
                user_perfil.save()

            return JsonResponse({'success': True, 'functions':'reload', 'message': jsonMessage}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ocurrió un error😯😥 <br>{str(e)}'}, status=400)
        
    yourBlogs = models.Articulos.objects.filter(autor = request.user)
    blogsTiple=[]
    for oneBlog in yourBlogs:
        blogsTiple.append({
            'id': oneBlog.id,
            'titulo': oneBlog.titulo,
        })
    
    return render(request, 'admin/blog.html', {'active_page':'blog','pages':functions.pages, 'blogsTiple':blogsTiple})

#Mapa ----------------------------------------------------------
@login_required
@never_cache
def map_page(request):
    categoria_mapa = models.Categorias.objects.get(categoria="Mapa")
    map_inDB = models.Database.objects.filter(categoria=categoria_mapa)
    UID = f'mapa-pleace_{models.generate_random_string(11)}'
    return render(request, 'admin/mapa.html', {'map_inDB': map_inDB, 'active_page': 'mapa', 'UID':UID,'pages': functions.pages})

@login_required
@never_cache
def update_create_pleace_map(request):
    if request.method != 'POST':
        # return JsonResponse({'error': 'Metodo no valido'}, status=400)
        return redirect('update_mapa')

    isNewPost = request.POST.get('isNew')
    uuidPost = request.POST.get('uuid')
    nombrePost = request.POST.get('nombreEdificio')
    colorPost = request.POST.get('colorEdificio')
    p1Post = request.POST.get('esquina1')
    p2Post = request.POST.get('esquina2')
    p3Post = request.POST.get('esquina3')
    p4Post = request.POST.get('esquina4')
    informacionText = request.POST.get('textTiny')
    informacionPost = request.POST.get('contenidoWord')
    door_cordsPost = request.POST.get('puertaCordsEdificio')
    imagenPost = request.FILES.get('fotoEdificio')

    with transaction.atomic():
        if isNewPost is None:
            if models.Mapa.objects.filter(uuid=uuidPost).exists():
                edificio = get_object_or_404(models.Mapa, uuid=uuidPost)
                edificio.nombre = nombrePost
                edificio.color = colorPost
                edificio.p1_polygons = p1Post
                edificio.p2_polygons = p2Post
                edificio.p3_polygons = p3Post
                edificio.p4_polygons = p4Post
                edificio.door_cords = door_cordsPost
                edificio.informacion = informacionPost
                edificio.uuid = uuidPost,
                edificio.save()
                success_message = f'Se Actualizaron los datos de <span>"{nombrePost}"</span> en el mapa de forma exitosa 🧐😁🎈'

            if imagenPost:
                map_database = get_object_or_404(models.Database, uuid=uuidPost)
                map_database.imagen = imagenPost
                map_database.save()
                success_message += '<br>Se actualizó su imagen en la Base de datos 😁🎉🎈'
            return JsonResponse({'success': True, 'message': success_message}, status=200)
        else:
            # validar si este ya existe en el mapa y en db para que no se repitan
            models.Mapa.objects.create(
                nombre=nombrePost,
                color=colorPost,
                p1_polygons=p1Post,
                p2_polygons=p2Post,
                p3_polygons=p3Post,
                p4_polygons=p4Post,
                door_cords=door_cordsPost,
                informacion=informacionPost,
                uuid=uuidPost,
            )
            
            # Verificar notas ToDo
            models.Database.objects.create(
                categoria=models.Categorias.objects.get(categoria="Mapa"),
                titulo=nombrePost,
                informacion=informacionText,
                imagen=imagenPost,
                uuid=uuidPost,
                evento_lugar='',
                evento_className='',
            )

            return JsonResponse({'success': True, 'message': 'Se creó un nuevo edificio en el mapa y en la base de datos de forma exitosa 🎉🎉🎉'}, status=200)

#Galeria ----------------------------------------------------------
@login_required
@never_cache
def upload_image(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES['file']
            imagen_articulo = models.Imagenes(imagen=image_file)
            imagen_articulo.save()
            image_url = imagen_articulo.imagen.url

            return JsonResponse({'location': image_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Error al subir la imagen'}, status=400)

@login_required
@never_cache
def lista_imagenes(request):
    imagenes = models.Imagenes.objects.all()
    imagenes_modificadas = []

    for imagen in imagenes:
        imagen_url = imagen.imagen.url
        imagenes_modificadas.append({
            'id': imagen.id,
            'url': imagen_url
        })
    return render(request, 'admin/blog_imgs.html', {'imagenes': imagenes_modificadas})
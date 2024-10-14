from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('cross_asistent.urls')),
    path('admin/', admin.site.urls),
]

handler400 = 'cross_asistent.views.error_400'
handler401 = 'cross_asistent.views.error_401'
handler403 = 'cross_asistent.views.error_403'
handler404 = 'cross_asistent.views.error_404'
handler405 = 'cross_asistent.views.error_405'
handler408 = 'cross_asistent.views.error_408'
handler429 = 'cross_asistent.views.error_429'
handler500 = 'cross_asistent.views.error_500'
handler502 = 'cross_asistent.views.error_502'
handler503 = 'cross_asistent.views.error_503'
handler504 = 'cross_asistent.views.error_504'
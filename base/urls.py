from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('page/<str:page_name>/', views.page, name='page'),
    path('selection/', views.selection_page, name='selection_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]

# обработка медиафайлов в urls.py проекта:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

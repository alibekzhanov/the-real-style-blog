from django.contrib import admin
from .models import Topics, Publication
from .forms import PublicationForm


# Кастомизированный класс для админской панели
class PublicationAdmin(admin.ModelAdmin):
    form = PublicationForm


# Регистрация моделей с кастомизированными админскими классами
admin.site.register(Topics)
admin.site.register(Publication, PublicationAdmin)


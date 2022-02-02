from django.contrib import admin
from .models import User
from reviews.models import Titles, Genres, Categories


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'category',
        'genre',
        'year'
    )
    list_editable = ('category',)
    search_fields = ('genre',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'

admin.site.register(User)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Categories, CategoriesAdmin)
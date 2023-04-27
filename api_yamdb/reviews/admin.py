from django.contrib import admin
from .models import Genre, Category, Title


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'description', 'category']
    filter_horizontal = ('genre',)

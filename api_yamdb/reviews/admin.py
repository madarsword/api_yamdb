from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'description', 'category']
    list_filter = ['name']
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'author', 'score']
    list_filter = ['pub_date']
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'text', 'author', 'pub_date']
    list_filter = ['review']
    empty_value_display = '-пусто-'

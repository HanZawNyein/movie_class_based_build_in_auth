from django.contrib import admin
from .models import Movie


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'release_date', 'status', 'created']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['created', 'status']
    list_editable = ['release_date', 'status']

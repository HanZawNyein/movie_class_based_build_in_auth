from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', login_required(views.AllMovies.as_view()), name="all_movies"),
    path('search/', login_required(views.AllMovies.as_view()), name="search_movies"),
    path('tag/<slug:tag_slug>/', login_required(views.AllMovies.as_view()), name='movie_by_tag'),
    path('details/<str:slug>/', login_required(views.MovieDetailView.as_view()), name="details")
]

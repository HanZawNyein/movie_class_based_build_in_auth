from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag

from .models import Movie


# Create your views here.
class AllMovies(ListView):
    model = Movie
    template_name = 'movie/list.html'
    context_object_name = 'movies'
    paginate_by = 10
    queryset = model.publish.all()


    def get_context_data(self, **kwargs):
        print(self.queryset)
        context = super().get_context_data(**kwargs)
        movies = self.queryset
        tag = None
        try:
            if self.kwargs['tag_slug']:
                tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
                movies = movies.filter(tags__in=[tag])
        except:
            pass
        try:
            search_value = self.request.GET['search']
            if search_value:
                movies = self.queryset.annotate(
                    similarity=TrigramSimilarity('name', search_value),
                ).filter(similarity__gt=0.1).order_by('-similarity')
        except:
            pass

        paginator = Paginator(movies, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            movies = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            movies = paginator.page(paginator.num_pages)
        context['movies'] = movies
        context['tag'] = tag
        return context


class MovieDetailView(ListView):
    model = Movie
    template_name = 'movie/details.html'
    movie = None

    def get_queryset(self):
        self.movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
        return self.movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_tags_ids = self.movie.tags.values_list('id', flat=True)
        similar_movies = Movie.publish.filter(tags__in=movie_tags_ids).exclude(id=self.movie.id)
        similar_movies = similar_movies.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
        context['movie'] = self.movie
        context['similar_movies'] = similar_movies
        return context

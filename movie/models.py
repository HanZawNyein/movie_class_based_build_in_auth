from django.db import models

# Create your models here.
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='publish')


class Movie(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    poster = models.ImageField(upload_to='posters/', blank=True)
    slug = models.SlugField()
    review = models.TextField()
    release_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('publish', 'PUBLISH')
    )
    status = models.CharField(max_length=250, choices=STATUS_CHOICES)

    objects = models.Manager()
    publish = PublishManager()
    tags = TaggableManager()

    class Meta:
        index_together = (('id', 'slug'),)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('movie:details', args=[self.slug])

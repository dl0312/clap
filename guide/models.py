from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from django.urls import reverse

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class TimeStampeModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', db_index=True)

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'pk': self.pk, })

    @property
    def get_images(self):
        return self.images.all()

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

class Post(TimeStampeModel):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title

class Image(TimeStampeModel):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_location)
    text = models.TextField(blank=True,null=True)
    tags = TaggableManager(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='images')

    @property
    def ancestor_query(self):
        return self.genre.get_ancestors

    def __str__(self):
        return '{} - {}'.format(self.title, self.text)




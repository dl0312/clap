from django.urls import path, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(
        regex = r'^$',
        view = views.image_list,
        name='image_list'
    ),
    url(
        regex = r'^genres/$',
        view = views.show_genres,
        name='show_genres'
    ),
    url(
        regex = r'^genres/(?P<genre>\w+)/$',
        view = views.genre_image,
        name='genre_image'
    ),
    url(
        regex = r'^image/new/$',
        view = views.image_new,
        name='image_new'
    ),
    url(
        regex = r'^image/(?P<pk>\d+)/$', 
        view = views.image_detail,
        name = 'image_detail' 
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

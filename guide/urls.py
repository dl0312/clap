from django.urls import path, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(
        regex = r'^$',
        view = views.post_list,
        name='post_list'
    ),
    url(
        regex = r'^api/post/$',
        view = views.Post.as_view(),
        name = 'api_post_list'
    ),
    url(
        regex = r'^api/image/$',
        view = views.Feed.as_view(),
        name = 'api_image_list'
    ),
    url(
        regex = r'^category/$',
        view = views.show_categories,
        name='show_categories'
    ),
    url(
        regex = r'^category/(?P<category>\w+)/$',
        view = views.category_image,
        name='category_image'
    ),
    url(
        regex = r'^post/new/$',
        view = views.post,
        name='post_new'
    ),
    url(
        regex = r'^post/new2/$',
        view = views.post_new,
        name='post_new'
    ),
    url(
        regex = r'^post/(?P<pk>\d+)/$', 
        view = views.post_detail,
        name = 'post_detail' 
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

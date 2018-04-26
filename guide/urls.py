from django.urls import path, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(
        regex = r'^users/explore/$',
        view = views.ExploreUsers.as_view(),
        name = 'api_explore_user'
    ),
    url(
        regex = r'^users/(?P<user_id>[0-9]+)/follow/$',
        view = views.FollowUser.as_view(),
        name = 'api_follow_user'
    ),
    url(
        regex = r'^users/(?P<user_id>[0-9]+)/unfollow/$',
        view = views.UnFollowUser.as_view(),
        name = 'api_unfollow_user'
    ),
    url(
        regex = r'^users/(?P<username>\w+)/followers/$',
        view = views.UserFollowers.as_view(),
        name = 'api_user_followers'
    ),
    url(
        regex = r'^users/(?P<username>\w+)/following/$',
        view = views.UserFollowing.as_view(),
        name = 'api_user_following'
    ),
    url(
        regex = r'^users/search/$',
        view = views.UserSearch.as_view(),
        name = 'api_user_search'
    ),
    url(
        regex = r'^users/push/$',
        view = views.RegisterPush.as_view(),
        name = 'api_push'
    ),
    url(
        regex = r'^users/(?P<username>\w+)/$',
        view = views.UserProfile.as_view(),
        name = 'api_user_profile'
    ),
    url(
        regex = r'^users/(?P<username>\w+)/password/$',
        view = views.ChangePassword.as_view(),
        name = 'api_change_password'
    ),
    url(
        regex = r'^users/login/facebook/$',
        view = views.FacebookLogin.as_view(),
        name = 'api_facebook_login'
    ),
    url(
        regex = r'^posts/$',
        view = views.PostList.as_view(),
        name = 'api_post_list'
    ),
    url(
        regex = r'^posts/(?P<post_id>[0-9]+)/$',
        view = views.Post.as_view(),
        name = 'api_post_detail'
    ),
    url(
        regex = r'^posts/(?P<post_id>[0-9]+)/claps/$',
        view = views.ClapPost.as_view(),
        name = 'api_clap_post'
    ),
    url(
        regex = r'^posts/(?P<post_id>[0-9]+)/comments/$',
        view = views.CommentOnPost.as_view(),
        name = 'api_comment_on_post'
    ),
    url(
        regex = r'^posts/(?P<post_id>[0-9]+)/comments/$',
        view = views.CommentOnPost.as_view(),
        name = 'api_comment_on_post'
    ),
    url(
        regex = r'^posts/tagsearch/$',
        view = views.PostTagSearch.as_view(),
        name = 'api_post_tag_search'
    ),
    url(
        regex = r'^posts/categorysearch/$',
        view = views.PostCategorySearch.as_view(),
        name = 'api_post_category_search'
    ),
    url(
        regex = r'^images/$',
        view = views.Feed.as_view(),
        name = 'api_image_list'
    ),
    url(
        regex = r'^category/$',
        view = views.CategoryList.as_view(),
        name = 'api_category_list'
    ),
    url(
        regex = r'^category/(?P<category>\w+)/$',
        view = views.ChildrenList.as_view(),
        name = 'api_child_category'
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

urlpatterns += [
    url(r'^', views.ReactAppView.as_view()),
]
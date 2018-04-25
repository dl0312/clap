from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category, Image
from django.contrib.auth.decorators import login_required
from .forms import ImageForm, PostForm
from django.shortcuts import redirect
from django.forms import modelformset_factory
from django.template import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from . import models, serializers
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os

class ReactAppView(View):

    def get(self, request):
        try:
            with open(os.path.join(str(settings.ROOT_DIR), 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except:
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status = 501,
            )


class PostList(APIView):

    def get(self, request, format=None):

        post_list = []

        posts = models.Post.objects.all()[:10]

        for post in posts:

            post_list.append(post)

        serializer = serializers.SimplePostSerializer(post_list, many=True, context={'request': request})

        return Response(serializer.data)

class Post(APIView):

    def find_own_post(self,post_id,user):
        try:
            post = models.Post.objects.get(id=post_id, creator=user)
            return post
        except models.Post.DoesNotExist:
            return None

    def post(self, request, format=None):

        user = request.user
        
        serializer = serializers.InputPostSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user)

            followers = user.follower.objects.all()
            
            for follower in followers:
    
                Notifications.create_notification(user,follower,"post",request.post,serializer.data['title'])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            
            print(serializer.errors)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id, format=None):

        user = request.user

        post = self.find_own_post(post_id,user)

        if post is None:
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializers.PostSerializer(post,context={'request':request})
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id, format=None):
        user=request.user
        post = self.find_own_post(post_id,user)
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializers = serializers.PostSerializer(post,context={'request':request})
        
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id, format=None):
        user = request.user
        post = self.find_own_post(post_id,user)
        if post is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClapPost(APIView):
    def post(self,request, post_id, format=None):
        
        user = request.user

        try:
            found_post = models.Post.objects.get(id=post_id)
        except models.Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user is found_post.creator:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        try:
            preexisting_clap = models.Clap.objects.get(
                creator = user,
                post = found_post
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except models.Clap.DoesNotExist:
            new_clap = models.Clap.objects.create(
                creator=user,
                post=found_post
            )

            Notifications.create_notification(user,found_post.creator,"clap",found_post)

            new_clap.save()
            
            return Response(status=status.HTTP_201_CREATED)

class Comment(APIView):

    def post(self, request, post_id, format=None):
        
        serializer = serializers.CommentSerializer(data=request.data)

        user = request.user

        try:
            found_post = models.Post.objects.get(id=post_id)
        except models.Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save(creator=user, post=found_post)
            Notifications.create_notification(user,found_post.creator,'comment',found_post,serializer.data['message'])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, format=None):

        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ModerateComment(APIView):

    def delete(self, request, post_id, comment_id, format=None):

        user = request.user
        
        try:
            comment_to_delete = models.Comment.objects.get(id=comment_id, post__id=post_id, post__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class Feed(APIView):
    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()
        post_list = []
        print(request.user.following.all())

        for following_user in following_users:
            user_posts = following_user.posts.all()[:2]
            for post in user_posts:
                post_list.append(post)

        my_posts = user.posts.all()[:2]
        for post in my_posts:
            post_list.append(post)
        sorted_list = sorted(post_list, key=lambda post: post.created_at, reverse=True)
        serializer = serializers.PostSerializer(sorted_list, many=True, context={'request': request})

        return Response(serializer.data)

class Notifications(APIView):

    def get(self,request, format=None):
        
        user = request.user

        notifications = models.Notification.objects.filter(to=user)

        serializer = serializers.NotificationSerializer(notifications, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create_notification(creator, to, notification_type, post = None, comment = None):

        notification = models.Notification.objects.create(
            creator = creator,
            to = to,
            notification_type = notification_type,
            post = post,
            comment = comment,
        )

class UserProfile(APIView):

    def get_user(self, username):

        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None
        
    def get(self, request, username, format=None):

        found_user = self.get_user(username)

        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.UserProfileSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format=None):

        user = request.user
        
        found_user = self.get_user(username)

        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif found_user.username !=user.username:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.UserProfileSerializer(found_user)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):

    def put(self, request, username, format=None):

        user = request.user
        
        if user.username == username:

            current_password = request.data.get('current_password', None)

            if current_password is not None:

                passwords_match = user.check_password(current_password)

                if passwords_match:
                    new_password = request.data.get('new_password', None)

                    if new_password is not None:
                        user.set_password(new_password)
                        user.save()

                        return Response(status=status.HTTP_200_OK)

                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class FollowUser(APIView):

    def post(self, request, user_id, format=None):
        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user.save()

        Notifications.create_notification(user,user_to_follow,'follow')

        return Response(status=status.HTTP_200_OK)

class UserFollower(APIView):

    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()

        serializer = serializers.ListUserSerializer(user_followers, many=True, context={"request":request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserFollowing(APIView):
    def get(self, request, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()

        serializer = serializers.ListUserSerializer(user_following)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UnFollowUser(APIView):

    def post(self,request, user_id, format=None):
        user = request.user
        
        try:
            user_to_unfollow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.following.remove(user_to_unfollow)
        user.save()
        return Response(status=status.HTTP_200_OK)



def post_list(request):
    posts = models.Post.objects.all()
    return render(request, 'guide/post_list.html', {'posts':posts})

def image_list(request):
    images = Image.objects.all()
    return render(request, 'guide/image_list.html', {'images':images})

def show_categories(request):
    return render(request, "guide/categories.html", {'categories': Category.objects.all()})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = PostForm()
    return render(request, 'guide/post_new.html',{'postForm':postForm, 'formset':formset})


@login_required
def post(request):
    ImageFormSet = modelformset_factory(Image,form=ImageForm, extra=3)

    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if postForm.is_valid() and formset.is_valid():

            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(post=post_form, image=image)
                photo.save()
            message.success(request,"check it out")
            return HttpResponseRedirect("/")
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'guide/post_new.html',{'postForm':postForm, 'formset':formset})

@login_required
def image_new(request):
    if request.method == "POST":
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user
            image.save()
            return redirect('image_detail', pk=image.pk)
    else:
        form = ImageForm()
    return render(request, 'guide/upload.html', {'form':form})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'guide/image_detail.html',{'image':image})
    
def post_detail(request, pk):
    post = get_object_or_404(Image, pk=pk)
    return render(request, 'guide/post_detail.html',{'post':post})

def category_image(request, genre):
    images = get_object_or_404(Genre, name=genre).get_images
    return render(request, 'guide/category_images.html',{'images':images})


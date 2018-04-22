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
from . import models, serializers

class Post(APIView):
    def get(self, request, format=None):
        post_list = []
        posts = models.Post.objects.all()
        for post in posts:
            post_list.append(post)
        serializer = serializers.PostSerializer(post_list, many=True, context={'request': request})
        return Response(serializer.data)

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


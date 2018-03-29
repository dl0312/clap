from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Genre, Image
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'guide/post_list.html', {'posts':posts})

def image_list(request):
    images = Image.objects.all()
    return render(request, 'guide/post_list.html', {'images':images})

def show_genres(request):
    return render(request, "guide/genres.html", {'genres': Genre.objects.all()})

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

def genre_image(request, genre):
    images = get_object_or_404(Genre, name=genre).get_images
    return render(request, 'guide/genre_images.html',{'images':images})


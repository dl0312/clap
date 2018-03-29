from django import forms
from .models import Post, Image, Genre

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','image','text','genre')
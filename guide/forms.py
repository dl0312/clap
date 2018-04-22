from django import forms
from .models import Post, Image, Category

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=245, label="Item Description.")

    class Meta:
        model = Post
        fields = ('title', 'category', 'body')

class ImageForm(forms.ModelForm):

    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ('post','image')
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
class TitleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title']

class ContentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
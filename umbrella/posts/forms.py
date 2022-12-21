from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']  # list of fields included in the form


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

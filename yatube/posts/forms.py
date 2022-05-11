from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        # Включение всех полей в форму:
        # fields = '__all__'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

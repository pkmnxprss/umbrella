from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=10, unique=True)
    description = models.TextField()

    # String representation of a class instance
    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    text = models.TextField(help_text='Post content')
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    # Special field for the optional image
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField('Publication date', auto_now_add=True)

    # Sort queryset at the model level
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Comment to "{self.post}" from "{self.author}"'


class Follow(models.Model):
    # A reference to the user object that is subscribing
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    # A reference to the user object being subscribed to
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        # Creating a link uniqueness so that there are no duplicates
        unique_together = ['user', 'author']

    def __str__(self):
        return f'"{self.user}" follows "{self.author}"'

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=10, unique=True)
    description = models.TextField()

    # string representation of a class instance
    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(help_text='Текст вашей записи', verbose_name='Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', blank=True, null=True,
                              verbose_name='Группа')
    # special field for the optional image
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    # # you can use this code to sort queryset at the model level
    # class Meta:
    #     ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Комментарий к посту {self.post} от {self.author}'


class Follow(models.Model):
    # a reference to the user object that is subscribing
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    # a reference to the user object being subscribed to
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        # creating a link uniqueness so that there are no duplicates
        unique_together = ['user', 'author']

    def __str__(self):
        return f'user: {self.user} -> author: {self.author}'

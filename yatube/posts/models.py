from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    # class Meta:
    #     ordering = ['-pub_date']
    text = models.TextField(
        help_text='Текст вашей записи',
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', blank=True, null=True,
                              verbose_name='Группа')
    # поле для картинки
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        # выводим текст поста
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    # В случае, если автор комментария или пост будут удалены — все привязанные
    # к ним комментарии должны автоматически удаляться.
    # Реализовано или нет?
    class Meta:
        ordering = ['-created']

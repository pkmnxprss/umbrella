from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Group, User, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


# Обратите внимание, что функция render возвращает специальный объект, который должна вернуть view-функция.
# Частая ошибка — вызывать функцию, но не передать результат ее выполнения в операторе return
def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


# view-функция для страницы сообщества
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = group.posts.all().order_by("-pub_date")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    response = render(request, "group.html", {"group": group,
                                              "page": page,
                                              "paginator": paginator})
    return response


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)  # Получаем объект <User> из запроса
    posts = Post.objects.filter(author=profile_user).order_by("-pub_date")  # Все посты конкретного пользователя
    posts_count = posts.count()  # Количество постов

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'profile.html', {'profile_user': profile_user,
                                            'posts_count': posts_count,
                                            'page': page,
                                            'paginator': paginator})


def post_view(request, username, post_id):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user)
    posts_count = posts.count()
    post = Post.objects.get(id=post_id)

    comments = Comment.objects.filter(post=post)

    form = CommentForm()

    return render(request, 'post.html', {'profile_user': profile_user,
                                         'posts_count': posts_count,
                                         'post': post,
                                         'items': comments,
                                         'form': form})


@login_required()
def post_new(request):
    """ Добавить новую запись, если пользователь известен. """
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'post_new.html', {'form': form, 'edit': False})
    form = PostForm()
    return render(request, 'post_new.html', {'form': form, 'edit': False})


@login_required()
def post_edit(request, username, post_id):
    """ Редактировать запись, если пользователь известен и является автором поста. """
    user_profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=user_profile)
    if request.user != user_profile:
        return redirect('post', username=username, post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username=request.user.username, post_id=post_id)

    return render(
        request, 'post_new.html', {'form': form, 'post': post, 'edit': True},
    )


# view-функция для обработки отправленного комментария (POST)
def add_comment(request, username, post_id):
    post_owner = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=post_owner)

    # По идее всегда POST
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post', username=username, post_id=post_id)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользовательской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)

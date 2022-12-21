from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm


# @cache_page(timeout=20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)  # show 10 posts per page
    page_number = request.GET.get('page')  # URL parameter with requested page number
    page = paginator.get_page(page_number)  # get records with desired offset
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator})


# Community page view-function
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)  # get a group instance by its slug, or throw a 404 error
    posts = group.posts.all().order_by("-pub_date")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group,
                                          "page": page,
                                          "paginator": paginator})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by("-pub_date")  # all posts owned by the user
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # Number of posts - paginator.count in the template.
    # Checking subscription to display on the page
    is_follow = False
    if request.user.is_authenticated:
        is_follow = request.user.follower.filter(author=profile_user).exists()

    # Count the number of subscriptions / subscribers
    followings_count = profile_user.follower.count()
    followers_count = profile_user.following.count()

    return render(request, 'profile.html', {'profile_user': profile_user,
                                            'page': page,
                                            'paginator': paginator,
                                            'is_follow': is_follow,
                                            'followers': followers_count,
                                            'followings': followings_count})


def post_view(request, username, post_id):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user)
    posts_count = posts.count()
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)  # get a queryset of comments for a post
    form = CommentForm()

    # Count the number of subscriptions / subscribers
    followings_count = profile_user.follower.count()
    followers_count = profile_user.following.count()

    return render(request, 'post.html', {'profile_user': profile_user,
                                         'posts_count': posts_count,
                                         'post': post,
                                         'items': comments,
                                         'form': form,
                                         'followers': followers_count,
                                         'followings': followings_count})


@login_required()
def post_new(request):
    """ Add a new post only if the user is known (logged in). """
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
    """ Edit the post only if the user is known (logged in) and is the author of the post. """
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


@login_required
# View function for processing posted comment (POST method)
def add_comment(request, username, post_id):
    post_owner = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=post_owner)
    author = get_object_or_404(User, username=request.user.username)
    # In principle, always POST
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post  # specify the post to which the comment is added
        comment.author = author  # specify the author of the comment as the user who sent the request
        comment.save()
    return redirect('post', username=username, post_id=post_id)


# View-function of the page where will be displayed the posts of the authors to which the current user is subscribed
@login_required
def follow_index(request):
    subs = get_object_or_404(User, username=request.user.username).follower.all()
    posts = Post.objects.filter(author__in=subs.values_list('author')).order_by('-pub_date')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page,
                                           'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author and author.following.filter(user=request.user).count() == 0:
        # Here we subscribe the user to another author
        Follow.objects.create(user=request.user, author=author).save()
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    # Here we unsubscribe the user to another author
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    # Exception variable contains debugging info, so we will not display it in the custom 404 page template
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)

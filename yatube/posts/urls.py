from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    path("new/", views.post_new, name="post_new"),
    path("group/<slug:slug>/", views.group_posts, name="group"),
    # В качестве адреса персональной страницы автора будет использоваться его username
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]

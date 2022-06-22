from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PostView, PostDetailView, CommentView, CommentDetailView, FollowViewSet, GroupView

router = SimpleRouter()
router.register('follow', FollowViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('posts/', PostView.as_view()),
    path('posts/<int:post_id>/', PostDetailView.as_view()),

    path('posts/<int:post_id>/comments/', CommentView.as_view()),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentDetailView.as_view()),

    path('group/', GroupView.as_view()),
]

urlpatterns += router.urls

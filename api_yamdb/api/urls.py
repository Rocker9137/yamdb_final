from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import APIUser, UserViewSetForAdmin
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSetForAdmin, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', APIUser.as_view(), name='me'),
    path('v1/', include(router_v1.urls)),
]

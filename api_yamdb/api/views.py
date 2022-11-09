from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Review, Title
from api.permissions import AuthorOrAdminOrReadOnly
from api.serializers import CommentSerializer, ReviewSerializer
from .firters import TitlesFilter
from .mixins import ListCreateDestroyGenericViewSet
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          ReadTitleSerializer, TitleSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для создания и получения отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для создания и получения комментария."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(ListCreateDestroyGenericViewSet):
    """Viewset для создания, получения и удаления категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyGenericViewSet):
    """Viewset для создания, получения и удаления жанра."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для создания, получения и удаления произведения."""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadTitleSerializer
        return TitleSerializer

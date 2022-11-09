from rest_framework import mixins, viewsets


class ListCreateDestroyGenericViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Пермишн позволяющий совершать не SELF_METHODS."""
    pass

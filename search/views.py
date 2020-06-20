from rest_framework import filters
from rest_framework import viewsets, mixins

from core.models import BibleVerseModel
from core.permissions import IsAdminOrReadOnly
from search import serializers



class BibleVerseViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = serializers.BibleVerseModelSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("book", "chapter", "verse", "text")
    ordering_fields = "__all__"
    queryset = BibleVerseModel.objects.order_by("id")

    def get_queryset(self):
        queryset = self.queryset
        return queryset
